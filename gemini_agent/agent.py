"""
Single Agent implementation with conversation management.

This module provides a simple agent wrapper that maintains conversation
history and provides a clean chat interface.
"""

import logging
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional

from .backend import GeminiBackend, StreamChunk

logger = logging.getLogger(__name__)


class Agent:
    """
    Single agent with conversation management.
    
    This class wraps the Gemini backend and manages:
    - Conversation history
    - System messages
    - Session state
    """
    
    def __init__(
        self,
        backend: GeminiBackend,
        agent_id: Optional[str] = None,
        system_message: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        """
        Initialize agent.
        
        Args:
            backend: GeminiBackend instance
            agent_id: Optional agent identifier
            system_message: Optional system message/prompt
            session_id: Optional session identifier
        """
        self.backend = backend
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.system_message = system_message or "You are a helpful AI assistant."
        self.session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        
        # Conversation history
        self.conversation_history: List[Dict[str, Any]] = []
        
        # Add system message to history
        self.conversation_history.append({
            "role": "system",
            "content": self.system_message
        })
        
        logger.info(f"✓ Agent initialized: {self.agent_id} (session: {self.session_id})")
    
    async def chat(
        self,
        user_message: str,
        stream: bool = True,
        **kwargs
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Send a message and get streaming response.
        
        Args:
            user_message: User's message
            stream: Whether to stream the response
            **kwargs: Additional generation parameters
        
        Yields:
            StreamChunk objects with response content
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get streaming response from backend
        full_response = ""
        async for chunk in self.backend.chat_stream(
            messages=self.conversation_history,
            **kwargs
        ):
            # Accumulate response content
            if chunk.type == "content" and chunk.content:
                full_response += chunk.content
            
            yield chunk
        
        # Add assistant response to history
        if full_response:
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
    
    async def chat_simple(self, user_message: str, **kwargs) -> str:
        """
        Non-streaming chat that returns complete response.
        
        Args:
            user_message: User's message
            **kwargs: Additional generation parameters
        
        Returns:
            Complete response text
        """
        full_response = ""
        async for chunk in self.chat(user_message, **kwargs):
            if chunk.type == "content" and chunk.content:
                full_response += chunk.content
        return full_response
    
    def reset(self):
        """Reset conversation history (keeps system message)."""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_message
        }]
        logger.info(f"🔄 Conversation history reset for {self.agent_id}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get current conversation history."""
        return self.conversation_history.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "message_count": len(self.conversation_history),
            "backend_model": self.backend.model_name,
        }


def create_agent(
    model: str = "gemini-2.0-flash-exp",
    system_message: Optional[str] = None,
    enable_code_execution: bool = False,
    enable_web_search: bool = False,
    api_key: Optional[str] = None,
    **kwargs
) -> Agent:
    """
    Convenient factory function to create an agent.
    
    Args:
        model: Gemini model name
        system_message: System prompt for the agent
        enable_code_execution: Enable code execution capability
        enable_web_search: Enable web search capability
        api_key: Google API key (or use env var)
        **kwargs: Additional backend configuration
    
    Returns:
        Configured Agent instance
    """
    backend = GeminiBackend(
        api_key=api_key,
        model=model,
        enable_code_execution=enable_code_execution,
        enable_web_search=enable_web_search,
        **kwargs
    )
    
    return Agent(
        backend=backend,
        system_message=system_message,
    )
