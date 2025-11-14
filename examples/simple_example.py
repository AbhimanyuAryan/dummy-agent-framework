#!/usr/bin/env python3
"""
Simple example: Using the agent programmatically.

This shows how to use the Gemini agent in your own Python code.
"""

import asyncio
from gemini_agent import create_agent


async def main():
    # Create agent with basic configuration
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a helpful AI assistant.",
    )
    
    print("🤖 Simple Agent Example\n")
    print("=" * 50)
    
    # Ask a question and get streaming response
    question = "What are the key principles of good software design?"
    print(f"\nQuestion: {question}\n")
    print("Response: ", end="", flush=True)
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    
    print("\n\n" + "=" * 50)
    
    # Ask a follow-up question (conversation history is maintained)
    follow_up = "Can you give me an example of the first principle?"
    print(f"\nFollow-up: {follow_up}\n")
    print("Response: ", end="", flush=True)
    
    async for chunk in agent.chat(follow_up):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    
    print("\n\n" + "=" * 50)
    print(f"\n✅ Conversation completed! Total messages: {len(agent.get_history())}")


if __name__ == "__main__":
    asyncio.run(main())
