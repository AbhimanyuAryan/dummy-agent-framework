#!/usr/bin/env python3
"""
Gemini Agent CLI - Simple command-line interface for Gemini agent.

Usage:
    # Interactive mode with config
    gemini-agent --config config.yaml
    
    # Single question with config
    gemini-agent --config config.yaml "What is the capital of France?"
    
    # Quick mode (no config)
    gemini-agent "What is 2+2?"
    
    # With model selection
    gemini-agent --model gemini-2.0-flash-exp "Explain quantum computing"
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .agent import create_agent
from .config import get_agent_config, get_ui_config, load_config

# Load environment variables
load_dotenv()

# Rich console for pretty output
console = Console()


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


async def interactive_mode(agent):
    """Run agent in interactive chat mode."""
    console.print("\n[bold green]Gemini Agent - Interactive Mode[/bold green]")
    console.print("[dim]Type 'exit', 'quit', or 'bye' to end the conversation[/dim]")
    console.print("[dim]Type 'reset' to clear conversation history[/dim]\n")
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if not user_input.strip():
                continue
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                console.print("\n[yellow]👋 Goodbye![/yellow]\n")
                break
            
            # Check for reset command
            if user_input.lower() == 'reset':
                agent.reset()
                console.print("\n[yellow]🔄 Conversation history cleared[/yellow]\n")
                continue
            
            # Get streaming response
            console.print("\n[bold green]Agent[/bold green]: ", end="")
            response_text = ""
            
            async for chunk in agent.chat(user_input):
                if chunk.type == "content" and chunk.content:
                    console.print(chunk.content, end="", style="white")
                    response_text += chunk.content
            
            console.print()  # New line after response
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 Interrupted. Goodbye![/yellow]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")


async def single_question_mode(agent, question: str):
    """Run agent with a single question."""
    console.print(Panel(
        f"[bold cyan]Question:[/bold cyan] {question}",
        border_style="cyan"
    ))
    
    console.print("\n[bold green]Response:[/bold green]\n")
    
    response_text = ""
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            console.print(chunk.content, end="", style="white")
            response_text += chunk.content
        elif chunk.type == "tool_call" and chunk.tool_calls:
            # Show tool usage
            for tool_call in chunk.tool_calls:
                if tool_call.get("type") == "code_execution":
                    console.print(f"\n\n[dim]Executing code ({tool_call.get('language', 'python')})...[/dim]\n")
    
    console.print("\n")


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Gemini Agent CLI - Simple orchestration with Google Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to ask (if not provided, enters interactive mode)"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to YAML configuration file"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.0-flash-exp",
        help="Gemini model to use (default: gemini-2.0-flash-exp)"
    )
    
    parser.add_argument(
        "--system-message",
        type=str,
        help="System message/prompt for the agent"
    )
    
    parser.add_argument(
        "--enable-code-execution",
        action="store_true",
        help="Enable code execution capability"
    )
    
    parser.add_argument(
        "--enable-web-search",
        action="store_true",
        help="Enable web search capability"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        help="Sampling temperature (0-2)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    try:
        # Load configuration if provided
        if args.config:
            console.print(f"[dim]Loading configuration from: {args.config}[/dim]")
            config = load_config(args.config)
            agent_config = get_agent_config(config)
            ui_config = get_ui_config(config)
        else:
            # Use command-line arguments
            agent_config = {
                'model': args.model,
                'system_message': args.system_message,
                'enable_code_execution': args.enable_code_execution,
                'enable_web_search': args.enable_web_search,
                'temperature': args.temperature,
            }
            ui_config = {'logging_enabled': args.verbose}
        
        # Create agent
        console.print(f"[dim]Initializing agent with model: {agent_config['model']}[/dim]")
        agent = create_agent(**agent_config)
        
        # Run in appropriate mode
        if args.question:
            # Single question mode
            await single_question_mode(agent, args.question)
        else:
            # Interactive mode
            await interactive_mode(agent)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        if args.verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


def cli_main():
    """Entry point for console script."""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
