#!/usr/bin/env python3
"""
Code execution example: Agent that can run Python code.

This demonstrates the code execution capability.
"""

import asyncio
from gemini_agent import create_agent


async def main():
    # Create agent with code execution enabled
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a helpful coding assistant. When solving problems, write and execute Python code to verify your solutions.",
        enable_code_execution=True,
    )
    
    print("🐍 Code Execution Example\n")
    print("=" * 50)
    
    # Ask the agent to solve a problem with code
    question = "Calculate the sum of all prime numbers between 1 and 100"
    print(f"\nQuestion: {question}\n")
    print("Response:\n")
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
        elif chunk.type == "tool_call" and chunk.tool_calls:
            for tool_call in chunk.tool_calls:
                if tool_call.get("type") == "code_execution":
                    print(f"\n\n[Executing {tool_call.get('language', 'Python')} code...]\n")
    
    print("\n\n" + "=" * 50)
    print("\n✅ Code execution example completed!")


if __name__ == "__main__":
    asyncio.run(main())
