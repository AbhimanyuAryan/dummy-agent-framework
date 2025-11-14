#!/usr/bin/env python3
"""
Comprehensive example showcasing all features of the Gemini Agent framework.

This example demonstrates:
1. Basic conversation
2. Code execution
3. Web search
4. Conversation history management
5. Configuration loading
6. Error handling
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from gemini_agent import create_agent
from gemini_agent.config import load_config, get_agent_config

# Load environment variables
load_dotenv()

console = Console()


async def demo_basic_conversation():
    """Demo 1: Basic conversation."""
    console.print("\n[bold cyan]Demo 1: Basic Conversation[/bold cyan]")
    console.print("─" * 60)
    
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a friendly AI assistant.",
    )
    
    question = "Tell me a fun fact about AI in 2 sentences."
    console.print(f"\n[yellow]Question:[/yellow] {question}\n")
    console.print("[green]Response:[/green] ", end="")
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
    
    console.print("\n")


async def demo_code_execution():
    """Demo 2: Code execution capability."""
    console.print("\n[bold cyan]Demo 2: Code Execution[/bold cyan]")
    console.print("─" * 60)
    
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a Python expert who writes and executes code.",
        enable_code_execution=True,
    )
    
    question = "Write Python code to calculate the factorial of 10"
    console.print(f"\n[yellow]Question:[/yellow] {question}\n")
    console.print("[green]Response:[/green]\n")
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
        elif chunk.type == "tool_call" and chunk.tool_calls:
            for tool_call in chunk.tool_calls:
                if tool_call.get("type") == "code_execution":
                    console.print(f"\n[dim]⚙️  Executing code...[/dim]\n", style="yellow")
    
    console.print("\n")


async def demo_web_search():
    """Demo 3: Web search capability."""
    console.print("\n[bold cyan]Demo 3: Web Search[/bold cyan]")
    console.print("─" * 60)
    
    agent = create_agent(
        model="gemini-2.5-pro",
        system_message="You are a research assistant with access to real-time information.",
        enable_web_search=True,
    )
    
    question = "What is the current status of the James Webb Space Telescope?"
    console.print(f"\n[yellow]Question:[/yellow] {question}\n")
    console.print("[green]Response:[/green] ", end="")
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
    
    console.print("\n")


async def demo_conversation_context():
    """Demo 4: Maintaining conversation context."""
    console.print("\n[bold cyan]Demo 4: Conversation Context[/bold cyan]")
    console.print("─" * 60)
    
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a helpful tutor.",
    )
    
    # First question
    console.print("\n[yellow]Question 1:[/yellow] What is machine learning?\n")
    console.print("[green]Response:[/green] ", end="")
    
    async for chunk in agent.chat("What is machine learning?"):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
    
    console.print("\n")
    
    # Follow-up question (uses context)
    console.print("\n[yellow]Question 2:[/yellow] Give me a simple example\n")
    console.print("[green]Response:[/green] ", end="")
    
    async for chunk in agent.chat("Give me a simple example"):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
    
    console.print("\n")
    
    # Show conversation history
    status = agent.get_status()
    console.print(f"[dim]📊 Conversation stats: {status['message_count']} messages[/dim]")


async def demo_config_loading():
    """Demo 5: Loading configuration from YAML."""
    console.print("\n[bold cyan]Demo 5: Configuration Loading[/bold cyan]")
    console.print("─" * 60)
    
    config_path = "config.yaml"
    if not Path(config_path).exists():
        console.print(f"\n[red]Config file not found: {config_path}[/red]")
        console.print("[yellow]Skipping this demo[/yellow]\n")
        return
    
    console.print(f"\n[dim]Loading config from: {config_path}[/dim]\n")
    
    config = load_config(config_path)
    agent_config = get_agent_config(config)
    
    agent = create_agent(**agent_config)
    
    question = "Hello! Can you introduce yourself?"
    console.print(f"[yellow]Question:[/yellow] {question}\n")
    console.print("[green]Response:[/green] ", end="")
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
    
    console.print("\n")


async def demo_error_handling():
    """Demo 6: Error handling."""
    console.print("\n[bold cyan]Demo 6: Error Handling[/bold cyan]")
    console.print("─" * 60)
    
    try:
        # Try to create agent without API key
        import os
        original_key = os.environ.get("GOOGLE_API_KEY")
        
        # Temporarily remove API key
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        
        console.print("\n[yellow]Attempting to create agent without API key...[/yellow]\n")
        agent = create_agent()
        
    except ValueError as e:
        console.print(f"[green]✓ Error caught correctly:[/green] {e}\n")
        
        # Restore API key
        if original_key:
            os.environ["GOOGLE_API_KEY"] = original_key
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}\n")


async def main():
    """Run all demos."""
    console.print(Panel.fit(
        "[bold green]Gemini Agent Framework[/bold green]\n"
        "[white]Comprehensive Feature Demonstration[/white]",
        border_style="green"
    ))
    
    demos = [
        ("Basic Conversation", demo_basic_conversation),
        ("Code Execution", demo_code_execution),
        ("Web Search", demo_web_search),
        ("Conversation Context", demo_conversation_context),
        ("Configuration Loading", demo_config_loading),
        ("Error Handling", demo_error_handling),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            await demo_func()
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Demo interrupted by user[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error in {name}:[/red] {e}\n")
            if "--verbose" in sys.argv:
                import traceback
                console.print(traceback.format_exc())
        
        if i < len(demos):
            console.print("\n[dim]Press Enter to continue to next demo...[/dim]", end="")
            input()
    
    console.print("\n" + "=" * 60)
    console.print("[bold green]✅ All demos completed![/bold green]")
    console.print("=" * 60)
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("1. Try interactive mode: [white]python -m gemini_agent.cli[/white]")
    console.print("2. Explore other examples in the examples/ directory")
    console.print("3. Read the README.md for full documentation\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted. Goodbye![/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]Fatal error:[/red] {e}\n")
        sys.exit(1)
