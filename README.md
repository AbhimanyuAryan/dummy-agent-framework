# Gemini Simple Agent

A lightweight single-agent orchestration framework using Google Gemini API.

## Features

- 🤖 **Simple Agent Orchestration**: Clean single-agent implementation with Gemini
- 💬 **Streaming Responses**: Real-time streaming chat responses
- 🔧 **Built-in Tools**: Support for code execution and web search
- 📝 **Conversation History**: Automatic conversation management
- ⚙️ **YAML Configuration**: Easy configuration via YAML files
- 🎨 **Rich CLI**: Beautiful terminal interface with Rich

## How to Run in PowerShell

### Setup (First Time Only)

1. Create a virtual environment:
```powershell
python -m venv gemini-agent
```

2. Copy and configure the environment file:
```powershell
cp .env.example .env
# Edit .env and add your Google API key from: https://aistudio.google.com/apikey
```

3. Activate the virtual environment and install dependencies:
```powershell
. gemini-agent\Scripts\activate.ps1
pip install -r requirements.txt
```

### Running the Agent

**Single Question Mode:**
```powershell
. gemini-agent\Scripts\activate.ps1
python -m gemini_agent.cli --model gemini-2.5-pro "Your question here"
```

**Interactive Mode:**
```powershell
. gemini-agent\Scripts\activate.ps1
python -m gemini_agent.cli --model gemini-2.5-pro
```

**With Configuration File:**
```powershell
. gemini-agent\Scripts\activate.ps1
python -m gemini_agent.cli --config config.yaml "Your question here"
```

**With Code Execution Enabled:**
```powershell
. gemini-agent\Scripts\activate.ps1
python -m gemini_agent.cli --model gemini-2.5-pro --enable-code-execution "Calculate the first 10 prime numbers"
```

**With Web Search Enabled:**
```powershell
. gemini-agent\Scripts\activate.ps1
python -m gemini_agent.cli --model gemini-2.5-pro --enable-web-search "What's the latest news on AI?"
```

## Installation

1. Clone or navigate to this directory:
```bash
cd dummy-agent-framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

Get your API key from: https://aistudio.google.com/apikey

## Quick Start

### Interactive Mode

Start a conversation with the agent:

```bash
python -m gemini_agent.cli --config config.yaml
```

Or if installed:
```bash
gemini-agent --config config.yaml
```

### Single Question Mode

Ask a single question:

```bash
python -m gemini_agent.cli --config config.yaml "What is the capital of France?"
```

### Without Configuration File

Quick usage without config:

```bash
python -m gemini_agent.cli "Explain quantum computing in simple terms"
```

With custom settings:
```bash
python -m gemini_agent.cli --model gemini-2.5-pro --enable-web-search "What's the latest news on AI?"
```

## Configuration

The framework uses YAML configuration files. See `config.yaml` for a basic example.

### Basic Configuration

```yaml
agent:
  id: "gemini-agent"
  
  backend:
    type: "gemini"
    model: "gemini-2.0-flash-exp"
    enable_code_execution: false
    enable_web_search: false
    temperature: 1.0
  
  system_message: "You are a helpful AI assistant."

ui:
  display_type: "rich_terminal"
  logging_enabled: true
```

### Example Configurations

The `examples/` directory contains several pre-configured setups:

- **`config_code_execution.yaml`**: Agent with Python code execution
- **`config_web_search.yaml`**: Agent with web search capability
- **`config_full_tools.yaml`**: Agent with all tools enabled

Try them:
```bash
python -m gemini_agent.cli --config examples/config_code_execution.yaml "Calculate fibonacci(20)"
```

## Usage Examples

### Code Execution

```bash
python -m gemini_agent.cli --config examples/config_code_execution.yaml
```

```
You: Calculate the first 10 prime numbers

Agent: [executes code and shows results]
```

### Web Search

```bash
python -m gemini_agent.cli --config examples/config_web_search.yaml
```

```
You: What's the current weather in Paris?

Agent: [searches web and provides current information]
```

### Custom System Message

```bash
python -m gemini_agent.cli --system-message "You are a Python expert" "How do I sort a dictionary by value?"
```

## Command-Line Options

```bash
python -m gemini_agent.cli --help
```

Options:
- `--config`: Path to YAML configuration file
- `--model`: Gemini model to use (default: gemini-2.0-flash-exp)
- `--system-message`: Custom system prompt
- `--enable-code-execution`: Enable code execution capability
- `--enable-web-search`: Enable web search capability
- `--temperature`: Sampling temperature (0-2)
- `--verbose`: Enable verbose logging

## Available Models

- `gemini-2.0-flash-exp` - Fast, efficient model (default)
- `gemini-2.5-pro` - More capable model for complex tasks
- `gemini-1.5-flash` - Previous generation flash model
- `gemini-1.5-pro` - Previous generation pro model

## Project Structure

```
dummy-agent-framework/
├── gemini_agent/
│   ├── __init__.py       # Package initialization
│   ├── agent.py          # Agent class with conversation management
│   ├── backend.py        # Gemini API wrapper
│   ├── cli.py            # Command-line interface
│   └── config.py         # Configuration loader
├── examples/
│   ├── config_code_execution.yaml
│   ├── config_web_search.yaml
│   └── config_full_tools.yaml
├── config.yaml           # Default configuration
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup
├── .env.example         # Environment template
└── README.md            # This file
```

## Key Components

### Agent Class
The `Agent` class manages conversation history and provides a simple chat interface:

```python
from gemini_agent import create_agent

agent = create_agent(
    model="gemini-2.0-flash-exp",
    system_message="You are a helpful assistant",
    enable_code_execution=True
)

# Streaming chat
async for chunk in agent.chat("Hello!"):
    if chunk.type == "content":
        print(chunk.content, end="")

# Simple chat (non-streaming)
response = await agent.chat_simple("What is 2+2?")
print(response)
```

### GeminiBackend Class
Low-level wrapper around the Google Gemini API:

```python
from gemini_agent.backend import GeminiBackend

backend = GeminiBackend(
    model="gemini-2.0-flash-exp",
    enable_code_execution=True,
    enable_web_search=True
)

async for chunk in backend.chat_stream(messages):
    print(chunk)
```

## Environment Variables

Create a `.env` file with:

```bash
GOOGLE_API_KEY=your_api_key_here
# or
GEMINI_API_KEY=your_api_key_here
```

## Interactive Mode Commands

When in interactive mode:
- `exit`, `quit`, `bye`, `q` - Exit the conversation
- `reset` - Clear conversation history

## Comparison with other frameworks

This framework is a simplified single-agent implementation based on other frameowork's architecture:

**Other frameworks** (Full Framework):
- Multi-agent coordination
- Binary decision voting system
- Advanced memory management
- Multiple LLM backend support
- Complex orchestration

**This Framework** (Simple Agent):
- Single agent only
- Gemini-specific
- Streamlined conversation management
- Easy to understand and extend
- Perfect for learning and simple use cases

## Development

Install in development mode:
```bash
pip install -e .
```

Run with verbose logging:
```bash
python -m gemini_agent.cli --verbose
```

## Troubleshooting

### API Key Issues
- Ensure your `GOOGLE_API_KEY` or `GEMINI_API_KEY` is set in `.env`
- Verify the key is valid at https://aistudio.google.com/apikey

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- If using Python 3.9-3.11, ensure compatibility with google-genai library

### Model Not Found
- Check available models in Google AI Studio
- Some models may require different access levels

## Contributing

This is a reference implementation. Feel free to:
- Add new features
- Improve error handling
- Add more examples
- Extend with custom tools

## License

MIT License - Feel free to use and modify

## Learn More

- [Google Gemini API Documentation](https://ai.google.dev/)
- [Rich Library Documentation](https://rich.readthedocs.io/)
