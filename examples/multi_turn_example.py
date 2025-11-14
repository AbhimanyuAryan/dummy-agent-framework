#!/usr/bin/env python3
"""
Multi-turn conversation example.

This demonstrates maintaining context across multiple exchanges.
"""

import asyncio
from gemini_agent import create_agent


async def ask_question(agent, question):
    """Helper to ask a question and print the response."""
    print(f"\n{'='*60}")
    print(f"You: {question}")
    print(f"{'='*60}\n")
    print("Agent: ", end="", flush=True)
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    
    print("\n")


async def main():
    # Create agent
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a knowledgeable tutor who explains concepts clearly.",
    )
    
    print("📚 Multi-Turn Conversation Example\n")
    
    # Have a multi-turn conversation about a topic
    await ask_question(agent, "What is recursion in programming?")
    await ask_question(agent, "Can you show me a simple example?")
    await ask_question(agent, "What are some common pitfalls to avoid?")
    await ask_question(agent, "How is this different from iteration?")
    
    # Show conversation stats
    print("=" * 60)
    status = agent.get_status()
    print(f"\n✅ Conversation completed!")
    print(f"   Total messages: {status['message_count']}")
    print(f"   Session ID: {status['session_id']}")
    print(f"   Agent ID: {status['agent_id']}\n")


if __name__ == "__main__":
    asyncio.run(main())
