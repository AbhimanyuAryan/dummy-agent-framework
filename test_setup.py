#!/usr/bin/env python3
"""
Quick test script to verify the installation.

Run this to check if everything is set up correctly.
"""

import asyncio
import os
import sys


def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment...\n")
    
    # Check Python version
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✓ API key found: {api_key[:10]}...")
    else:
        print("❌ API key not found!")
        print("   Please set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file")
        return False
    
    # Try importing dependencies
    try:
        import google.genai
        print("✓ google-genai imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import google-genai: {e}")
        return False
    
    try:
        from rich.console import Console
        print("✓ rich imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import rich: {e}")
        return False
    
    try:
        import yaml
        print("✓ PyYAML imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import yaml: {e}")
        return False
    
    return True


async def test_agent():
    """Test basic agent functionality."""
    print("\n🤖 Testing agent...\n")
    
    try:
        from gemini_agent import create_agent
        
        # Create a simple agent
        agent = create_agent(
            model="gemini-2.0-flash-exp",
            system_message="You are a helpful assistant.",
        )
        
        print("✓ Agent created successfully")
        
        # Test a simple question
        print("\nAsking: 'Say hello in exactly 3 words'")
        print("Response: ", end="", flush=True)
        
        response = ""
        async for chunk in agent.chat("Say hello in exactly 3 words"):
            if chunk.type == "content" and chunk.content:
                response += chunk.content
                print(chunk.content, end="", flush=True)
        
        print("\n\n✓ Agent responded successfully!")
        
        # Check status
        status = agent.get_status()
        print(f"\nAgent Status:")
        print(f"  - Agent ID: {status['agent_id']}")
        print(f"  - Model: {status['backend_model']}")
        print(f"  - Messages: {status['message_count']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing agent: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    print("=" * 60)
    print("Gemini Agent Framework - Installation Test")
    print("=" * 60)
    print()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed!")
        print("\nPlease ensure:")
        print("1. You have run: pip install -r requirements.txt")
        print("2. You have set GOOGLE_API_KEY in your .env file")
        print("3. Your API key is valid")
        sys.exit(1)
    
    # Test agent
    if not await test_agent():
        print("\n❌ Agent test failed!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Your setup is working correctly.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Try interactive mode: python -m gemini_agent.cli")
    print("2. Run examples: python examples/simple_example.py")
    print("3. Read the README.md for more information")
    print()


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(main())
