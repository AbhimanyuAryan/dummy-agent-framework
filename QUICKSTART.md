# Gemini Simple Agent - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Get your API key from: https://aistudio.google.com/apikey

Then create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Test Installation

```bash
python test_setup.py
```

### 4. Run Interactive Mode

```bash
python -m gemini_agent.cli
```

## 📚 Usage Examples

### Interactive Chat
```bash
python -m gemini_agent.cli
```

### Single Question
```bash
python -m gemini_agent.cli "What is the capital of France?"
```

### With Configuration
```bash
python -m gemini_agent.cli --config config.yaml "Hello!"
```

### Code Execution
```bash
python -m gemini_agent.cli --config examples/config_code_execution.yaml
```

### Web Search
```bash
python -m gemini_agent.cli --config examples/config_web_search.yaml
```

## 🎯 Example Scripts

Run the example scripts to see the framework in action:

```bash
# Basic example
python examples/simple_example.py

# Code execution
python examples/code_execution_example.py

# Web search
python examples/web_search_example.py

# Multi-turn conversation
python examples/multi_turn_example.py
```

## 🛠️ Programmatic Usage

```python
import asyncio
from gemini_agent import create_agent

async def main():
    # Create agent
    agent = create_agent(
        model="gemini-2.0-flash-exp",
        system_message="You are a helpful assistant",
    )
    
    # Stream responses
    async for chunk in agent.chat("Hello!"):
        if chunk.type == "content":
            print(chunk.content, end="")

asyncio.run(main())
```

## 🎨 Available Models

- `gemini-2.0-flash-exp` - Fast & efficient (recommended)
- `gemini-2.5-pro` - Most capable
- `gemini-1.5-flash` - Previous generation
- `gemini-1.5-pro` - Previous generation

## 🔧 Configuration

Edit `config.yaml` or create your own:

```yaml
agent:
  backend:
    model: "gemini-2.0-flash-exp"
    enable_code_execution: true
    enable_web_search: true
  system_message: "You are a helpful assistant"
```

## 📖 Learn More

See [README.md](README.md) for complete documentation.

## 🐛 Troubleshooting

**Import errors?**
```bash
pip install -r requirements.txt
```

**API key issues?**
- Check `.env` file exists
- Verify key is correct
- Try setting directly: `export GOOGLE_API_KEY=your_key`

**Module not found?**
```bash
pip install -e .
```
