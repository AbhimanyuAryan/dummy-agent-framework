# Tutorial: Building with Gemini Agent Framework

This tutorial will guide you through using the Gemini Agent Framework, from basic setup to advanced features.

## Part 1: Getting Started (5 minutes)

### Step 1: Install the Framework

```bash
# Clone or navigate to the directory
cd dummy-agent-framework

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Your API Key

1. Get your API key from https://aistudio.google.com/apikey
2. Create a `.env` file:

```bash
cp .env.example .env
```

3. Edit `.env` and add your key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 3: Test Your Setup

```bash
python test_setup.py
```

If all checks pass ✅, you're ready to go!

## Part 2: Your First Agent (10 minutes)

### Interactive Chat

Let's start with the simplest way to use the framework:

```bash
python -m gemini_agent.cli
```

This launches interactive mode. Try:
- Ask a question: "What is Python?"
- Ask a follow-up: "Give me an example"
- Type `reset` to clear history
- Type `exit` to quit

### Single Questions

For one-off questions:

```bash
python -m gemini_agent.cli "Explain quantum entanglement in simple terms"
```

The agent will respond and exit.

## Part 3: Using Configuration Files (15 minutes)

### Create Your First Config

Create `my_config.yaml`:

```yaml
agent:
  id: "my-assistant"
  
  backend:
    type: "gemini"
    model: "gemini-2.0-flash-exp"
    temperature: 0.7
  
  system_message: "You are a helpful coding assistant specializing in Python."

ui:
  display_type: "rich_terminal"
  logging_enabled: true
```

### Use Your Config

```bash
python -m gemini_agent.cli --config my_config.yaml "How do I sort a list in Python?"
```

The agent will use your custom system message and settings.

### Try Pre-made Configs

```bash
# Code execution
python -m gemini_agent.cli --config examples/config_code_execution.yaml

# Web search
python -m gemini_agent.cli --config examples/config_web_search.yaml

# All tools
python -m gemini_agent.cli --config examples/config_full_tools.yaml
```

## Part 4: Programming with the Agent (20 minutes)

### Basic Programmatic Usage

Create `my_first_agent.py`:

```python
import asyncio
from gemini_agent import create_agent

async def main():
    # Create an agent
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a helpful assistant.",
    )
    
    # Ask a question with streaming
    print("Question: What is recursion?\n")
    print("Answer: ", end="", flush=True)
    
    async for chunk in agent.chat("What is recursion?"):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python my_first_agent.py
```

### Multi-Turn Conversations

Create `conversation.py`:

```python
import asyncio
from gemini_agent import create_agent

async def ask(agent, question):
    """Helper to ask and print response."""
    print(f"\nYou: {question}")
    print("Agent: ", end="", flush=True)
    
    async for chunk in agent.chat(question):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    print("\n")

async def main():
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a patient tutor.",
    )
    
    # Have a multi-turn conversation
    await ask(agent, "What is machine learning?")
    await ask(agent, "Can you give an example?")
    await ask(agent, "How is it different from traditional programming?")
    
    # Show stats
    status = agent.get_status()
    print(f"Conversation had {status['message_count']} messages")

if __name__ == "__main__":
    asyncio.run(main())
```

### Non-Streaming Responses

For simpler code, use `chat_simple()`:

```python
import asyncio
from gemini_agent import create_agent

async def main():
    agent = create_agent()
    
    # Get complete response at once
    response = await agent.chat_simple("What is 2+2?")
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Part 5: Code Execution (15 minutes)

### Enable Code Execution

Create `code_agent.py`:

```python
import asyncio
from gemini_agent import create_agent

async def main():
    # Enable code execution
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a Python expert. Use code execution to solve problems.",
        enable_code_execution=True,  # ← Key setting
    )
    
    print("Asking agent to calculate prime numbers...\n")
    
    async for chunk in agent.chat("Find all prime numbers between 1 and 50"):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
        elif chunk.type == "tool_call":
            print("\n[Agent is executing code...]\n")
    
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python code_agent.py
```

The agent will write Python code and execute it to solve the problem!

### Code Execution Tasks

Try these questions with code execution enabled:

1. "Calculate the Fibonacci sequence up to the 20th term"
2. "Generate a random 10x10 matrix and find its determinant"
3. "Create a histogram of word frequencies in this text: ..."
4. "Calculate the first 100 digits of Pi"

## Part 6: Web Search (15 minutes)

### Enable Web Search

Create `search_agent.py`:

```python
import asyncio
from gemini_agent import create_agent

async def main():
    # Enable web search
    agent = create_agent(
        model="gemini-2.5-pro",  # Pro model recommended for search
        system_message="You are a research assistant with web access.",
        enable_web_search=True,  # ← Enable search
    )
    
    print("Asking about current events...\n")
    
    async for chunk in agent.chat("What are the latest developments in AI this week?"):
        if chunk.type == "content" and chunk.content:
            print(chunk.content, end="", flush=True)
    
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
```

### Web Search Tasks

Try these questions:

1. "What's the current weather in Tokyo?"
2. "Latest news on renewable energy"
3. "Who won the latest Nobel Prize in Physics?"
4. "Current stock price of NVIDIA"

## Part 7: Advanced Features (20 minutes)

### Loading Configuration from Code

```python
import asyncio
from gemini_agent.config import load_config, get_agent_config
from gemini_agent import create_agent

async def main():
    # Load config from YAML
    config = load_config("config.yaml")
    agent_config = get_agent_config(config)
    
    # Create agent from config
    agent = create_agent(**agent_config)
    
    response = await agent.chat_simple("Hello!")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### Managing Conversation History

```python
import asyncio
from gemini_agent import create_agent

async def main():
    agent = create_agent()
    
    # Have a conversation
    await agent.chat_simple("My name is Alice")
    await agent.chat_simple("What's the capital of France?")
    
    # Get conversation history
    history = agent.get_history()
    print(f"Conversation has {len(history)} messages")
    
    # Print history
    for msg in history:
        print(f"{msg['role']}: {msg['content'][:50]}...")
    
    # Reset conversation
    agent.reset()
    print(f"After reset: {len(agent.get_history())} messages")

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling

```python
import asyncio
from gemini_agent import create_agent

async def main():
    try:
        agent = create_agent()
        response = await agent.chat_simple("Hello!")
        print(response)
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom System Messages for Different Tasks

```python
import asyncio
from gemini_agent import create_agent

async def create_specialist_agent(specialty):
    """Create an agent specialized for a specific task."""
    
    prompts = {
        "code_reviewer": "You are an expert code reviewer. Analyze code for bugs, performance issues, and best practices.",
        "teacher": "You are a patient teacher who explains concepts clearly with examples.",
        "writer": "You are a creative writer who helps with storytelling and editing.",
        "data_analyst": "You are a data analyst who helps interpret data and create insights.",
    }
    
    return create_agent(
        model="gemini-2.0-flash-exp",
        system_message=prompts.get(specialty, "You are a helpful assistant."),
        enable_code_execution=(specialty == "data_analyst"),
    )

async def main():
    # Create a code reviewer
    reviewer = await create_specialist_agent("code_reviewer")
    
    code = """
    def calculate_sum(numbers):
        total = 0
        for i in range(len(numbers)):
            total = total + numbers[i]
        return total
    """
    
    response = await reviewer.chat_simple(f"Review this code:\n{code}")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Part 8: Putting It All Together (30 minutes)

### Build a Complete Application

Create `assistant_app.py`:

```python
import asyncio
from gemini_agent import create_agent
from rich.console import Console
from rich.panel import Panel

console = Console()

async def main():
    console.print(Panel(
        "[bold green]My Personal AI Assistant[/bold green]\n"
        "Powered by Gemini Agent Framework",
        border_style="green"
    ))
    
    # Create agent with all features
    agent = create_agent(
        model="gemini-2.5-pro",
        system_message=(
            "You are a personal AI assistant. You can:\n"
            "- Execute Python code to solve problems\n"
            "- Search the web for current information\n"
            "- Remember our conversation context\n"
            "Be helpful, accurate, and concise."
        ),
        enable_code_execution=True,
        enable_web_search=True,
    )
    
    console.print("\n[cyan]Commands:[/cyan]")
    console.print("  /status - Show agent status")
    console.print("  /reset  - Clear conversation")
    console.print("  /exit   - Quit")
    console.print()
    
    while True:
        try:
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ")
            
            if not user_input.strip():
                continue
            
            # Handle commands
            if user_input.lower() in ['/exit', '/quit']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if user_input.lower() == '/reset':
                agent.reset()
                console.print("[green]Conversation reset[/green]")
                continue
            
            if user_input.lower() == '/status':
                status = agent.get_status()
                console.print(f"[green]Agent:[/green] {status['agent_id']}")
                console.print(f"[green]Model:[/green] {status['backend_model']}")
                console.print(f"[green]Messages:[/green] {status['message_count']}")
                continue
            
            # Get response
            console.print("\n[bold green]Assistant:[/bold green] ", end="")
            
            async for chunk in agent.chat(user_input):
                if chunk.type == "content" and chunk.content:
                    console.print(chunk.content, end="")
                elif chunk.type == "tool_call":
                    console.print("\n[dim][Processing...][/dim]\n", end="")
            
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Use /exit to quit.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())
```

Run your complete application:
```bash
python assistant_app.py
```

## Next Steps

### Experiment with Different Configurations

1. Try different models:
   - `gemini-2.0-flash-exp` - Fast and efficient
   - `gemini-2.5-pro` - More capable

2. Adjust temperature:
   - Lower (0.3-0.7) for factual responses
   - Higher (0.8-1.5) for creative responses

3. Customize system messages for different personas

### Extend the Framework

1. Add persistent storage (save conversations)
2. Add token counting and cost tracking
3. Integrate with other tools or APIs
4. Build a web interface with FastAPI
5. Add support for images/files

### Learn from Examples

Run all the example scripts:

```bash
python examples/simple_example.py
python examples/code_execution_example.py
python examples/web_search_example.py
python examples/multi_turn_example.py
python examples/full_demo.py
```

### Read the Documentation

- `README.md` - Complete reference
- `ARCHITECTURE.md` - System design
- `PROJECT_SUMMARY.md` - Overview

## Common Patterns

### Pattern 1: Question-Answer Bot

```python
async def qa_bot(question):
    agent = create_agent(system_message="You provide concise answers.")
    return await agent.chat_simple(question)
```

### Pattern 2: Code Assistant

```python
async def code_helper():
    return create_agent(
        system_message="You help with coding questions.",
        enable_code_execution=True,
    )
```

### Pattern 3: Research Assistant

```python
async def researcher():
    return create_agent(
        model="gemini-2.5-pro",
        system_message="You research topics thoroughly.",
        enable_web_search=True,
    )
```

## Troubleshooting

### API Key Issues
```python
import os
print(os.getenv("GOOGLE_API_KEY"))  # Should print your key
```

### Import Errors
```bash
pip install --upgrade google-genai rich pyyaml python-dotenv
```

### Async Issues
```python
import nest_asyncio
nest_asyncio.apply()  # If running in Jupyter/existing event loop
```

## Conclusion

You now know how to:
- ✅ Set up and configure the framework
- ✅ Use the CLI for quick interactions
- ✅ Build programmatic agents
- ✅ Enable code execution and web search
- ✅ Manage conversation history
- ✅ Create specialized agents for different tasks

Happy building! 🚀
