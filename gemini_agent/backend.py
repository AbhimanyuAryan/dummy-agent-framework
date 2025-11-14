"""
Simplified Gemini Backend for single agent orchestration.

This module provides a clean wrapper around the Google Gemini API,
supporting streaming responses, code execution, and web search.
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, List, Optional

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


@dataclass
class StreamChunk:
    """Represents a chunk of streaming response."""
    
    type: str  # "content", "tool_call", "done"
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class GeminiBackend:
    """
    Simplified Gemini backend for single agent use.
    
    Features:
    - Streaming responses
    - Code execution support
    - Web search/grounding
    - Conversation history management
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.0-flash-exp",
        enable_code_execution: bool = False,
        enable_web_search: bool = False,
        **kwargs
    ):
        """
        Initialize Gemini backend.
        
        Args:
            api_key: Google API key (or set GOOGLE_API_KEY env var)
            model: Model name (default: gemini-2.0-flash-exp)
            enable_code_execution: Enable code execution tool
            enable_web_search: Enable Google Search grounding
            **kwargs: Additional model configuration
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key required. Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
        
        self.model_name = model
        self.enable_code_execution = enable_code_execution
        self.enable_web_search = enable_web_search
        self.config = kwargs
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        logger.info(f"✓ Gemini backend initialized with model: {model}")
        if enable_code_execution:
            logger.info("  - Code execution: ENABLED")
        if enable_web_search:
            logger.info("  - Web search: ENABLED")
    
    def _build_tools_config(self) -> Optional[types.Tool]:
        """Build tools configuration for Gemini API."""
        tools = []
        
        if self.enable_code_execution:
            tools.append({"code_execution": {}})
        
        if self.enable_web_search:
            tools.append({"google_search": {}})
        
        return tools if tools else None
    
    def _format_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format messages for Gemini API.
        
        Gemini expects:
        - role: "user" or "model"
        - parts: list of content parts
        """
        formatted = []
        
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            
            # Skip system messages - they should be handled separately
            if role == "system":
                continue
            
            # Convert "assistant" to "model" for Gemini
            if role == "assistant":
                role = "model"
            
            formatted_msg = {
                "role": role,
                "parts": [{"text": content}]
            }
            formatted.append(formatted_msg)
        
        return formatted
    
    def _extract_system_message(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        """Extract system message from messages list."""
        for msg in messages:
            if msg.get("role") == "system":
                return msg.get("content")
        return None
    
    async def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Stream chat responses from Gemini.
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional generation parameters
        
        Yields:
            StreamChunk objects with response content
        """
        # Extract system instruction
        system_instruction = self._extract_system_message(messages)
        
        # Format messages for Gemini
        formatted_messages = self._format_messages(messages)
        
        # Build generation config
        generation_config = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if max_tokens is not None:
            generation_config["max_output_tokens"] = max_tokens
        
        # Merge with any additional config
        generation_config.update(self.config)
        generation_config.update(kwargs)
        
        # Build tools config
        tools = self._build_tools_config()
        
        try:
            # Create the generation request
            request_params = {
                "model": self.model_name,
                "contents": formatted_messages,
            }
            
            if system_instruction:
                request_params["config"] = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=generation_config.get("temperature"),
                    max_output_tokens=generation_config.get("max_output_tokens"),
                    tools=tools,
                )
            elif generation_config or tools:
                request_params["config"] = types.GenerateContentConfig(
                    temperature=generation_config.get("temperature"),
                    max_output_tokens=generation_config.get("max_output_tokens"),
                    tools=tools,
                )
            
            # Stream the response
            full_response = ""
            stream = await self.client.aio.models.generate_content_stream(**request_params)
            async for chunk in stream:
                # Extract text from chunk
                if chunk.text:
                    full_response += chunk.text
                    yield StreamChunk(
                        type="content",
                        content=chunk.text,
                        metadata={
                            "model": self.model_name,
                        }
                    )
                
                # Check for function calls/tool usage
                if hasattr(chunk, 'candidates') and chunk.candidates:
                    candidate = chunk.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            # Code execution results
                            if hasattr(part, 'executable_code') and part.executable_code:
                                yield StreamChunk(
                                    type="tool_call",
                                    tool_calls=[{
                                        "type": "code_execution",
                                        "code": part.executable_code.code,
                                        "language": part.executable_code.language,
                                    }],
                                )

                            # Code execution output
                            if hasattr(part, 'code_execution_result') and part.code_execution_result:
                                result_text = f"\n```\nCode execution result:\n{part.code_execution_result.output}\n```\n"
                                yield StreamChunk(
                                    type="content",
                                    content=result_text,
                                    metadata={"tool_result": True}
                                )
            
            # Yield final done chunk
            yield StreamChunk(
                type="done",
                metadata={
                    "model": self.model_name,
                    "total_length": len(full_response),
                }
            )
            
        except Exception as e:
            logger.error(f"Error in Gemini chat stream: {e}")
            yield StreamChunk(
                type="error",
                content=f"Error: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> str:
        """
        Non-streaming chat (collects all chunks).
        
        Args:
            messages: List of conversation messages
            **kwargs: Additional generation parameters
        
        Returns:
            Complete response text
        """
        full_response = ""
        async for chunk in self.chat_stream(messages, **kwargs):
            if chunk.type == "content" and chunk.content:
                full_response += chunk.content
        return full_response
