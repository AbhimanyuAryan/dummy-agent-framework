#!/usr/bin/env python3
"""
Web search example: Agent that can search the web.

This demonstrates the web search capability.
"""

import asyncio
from gemini_agent import create_agent


async def main():
    # Create agent with web search enabled
    agent = create_agent(
        model="gemini-2.5-pro",  # Using Pro model for better search integration
        system_message="You are a research assistant with access to real-time web search. Provide accurate, up-to-date information.",
        enable_web_search=True,
    )
    
    print("🔍 Web Search Example\n")
    print("=" * 50)
    
    # Ask about current events (requires web search)
    question = "What are the latest developments in AI technology this week?"
    print(f"\nQuestion: {question}\n")
    print("Response:\n")
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    
    print("\n\n" + "=" * 50)
    print("\n✅ Web search example completed!")


if __name__ == "__main__":
    asyncio.run(main())
