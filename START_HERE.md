# 🎯 START HERE - Gemini Simple Agent Framework

## 🚀 What Is This?

A **complete, production-ready single-agent framework** using Google Gemini API.

Perfect for:
- 📚 **Learning** how to build AI agents
- 🔨 **Prototyping** agent-based applications
- 🎓 **Understanding** LLM API integration
- 🚀 **Quick projects** with Gemini

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup API Key
```bash
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```
Get your key: https://aistudio.google.com/apikey

### 3️⃣ Run
```bash
python -m gemini_agent.cli
```

That's it! You now have a working AI agent.

## 💬 Try These Commands

**Interactive chat:**
```bash
python -m gemini_agent.cli
```

**Ask a question:**
```bash
python -m gemini_agent.cli "Explain quantum computing"
```

**With code execution:**
```bash
python -m gemini_agent.cli --config examples/config_code_execution.yaml
```

**Run an example:**
```bash
python examples/simple_example.py
```

## 📚 Documentation

Choose your path:

| I want to... | Read this... | Time |
|-------------|-------------|------|
| **Get started NOW** | [QUICKSTART.md](QUICKSTART.md) | 5 min |
| **Learn step-by-step** | [TUTORIAL.md](TUTORIAL.md) | 60 min |
| **Understand everything** | [README.md](README.md) | 20 min |
| **See all docs** | [INDEX.md](INDEX.md) | 5 min |

## ✨ Key Features

- ✅ **Streaming responses** - Real-time output
- ✅ **Code execution** - Run Python code
- ✅ **Web search** - Access real-time info
- ✅ **Easy config** - YAML-based setup
- ✅ **Beautiful CLI** - Rich terminal UI
- ✅ **Full examples** - 5+ working scripts

## 📁 What's Inside

```
dummy-agent-framework/
├── 📚 Documentation/        7 comprehensive guides
├── 💻 gemini_agent/         Core framework code
├── 📝 examples/             5+ working examples
├── ⚙️  config.yaml          Default configuration
└── 🧪 test_setup.py         Installation test
```

**29 files total** | **108 KB** | **~5,000 lines**

## 🎯 Use Cases

### 1. Simple Chat Bot
```bash
python -m gemini_agent.cli
```

### 2. Code Helper
```bash
python -m gemini_agent.cli --enable-code-execution "Calculate fibonacci(20)"
```

### 3. Research Assistant
```bash
python -m gemini_agent.cli --enable-web-search "Latest AI news"
```

### 4. Custom Application
```python
from gemini_agent import create_agent

agent = create_agent(
    model="gemini-2.0-flash-exp",
    enable_code_execution=True,
)

async for chunk in agent.chat("Your question"):
    print(chunk.content, end="")
```

## 🔧 Configuration

Edit `config.yaml`:

```yaml
agent:
  backend:
    model: "gemini-2.0-flash-exp"
    enable_code_execution: true
    enable_web_search: true
  system_message: "You are a helpful assistant"
```

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Files** | 29 |
| **Code Lines** | ~750 Python |
| **Docs Lines** | ~4,500 Markdown |
| **Examples** | 5 working scripts |
| **Dependencies** | 6 core packages |
| **Documentation** | 7 comprehensive files |

## 🎓 What You'll Learn

1. ✅ How to wrap LLM APIs
2. ✅ Async/await patterns
3. ✅ Streaming responses
4. ✅ CLI design
5. ✅ Configuration systems
6. ✅ Clean architecture

## 🚦 Next Steps

### Beginner Path
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `python test_setup.py`
3. Try `python -m gemini_agent.cli`
4. Run `python examples/simple_example.py`

### Learner Path
1. Work through [TUTORIAL.md](TUTORIAL.md)
2. Run all examples
3. Read [ARCHITECTURE.md](ARCHITECTURE.md)
4. Build your own app

### Developer Path
1. Study the source code
2. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Extend the framework
4. Contribute improvements

## 🆘 Need Help?

1. **Setup issues?** → Run `python test_setup.py`
2. **Don't know where to start?** → Read [QUICKSTART.md](QUICKSTART.md)
3. **Want to learn?** → Follow [TUTORIAL.md](TUTORIAL.md)
4. **Need reference?** → Check [README.md](README.md)
5. **Can't find docs?** → See [INDEX.md](INDEX.md)

## 🎁 What's Included

### Core Framework (5 files)
- ✅ Gemini API wrapper
- ✅ Agent implementation
- ✅ CLI interface
- ✅ Configuration loader
- ✅ Package setup

### Documentation (7 files)
- ✅ Quick start guide
- ✅ Complete tutorial
- ✅ Full reference
- ✅ Architecture guide
- ✅ Project summary
- ✅ Documentation index
- ✅ MIT License

### Examples (5+ files)
- ✅ Simple usage
- ✅ Code execution
- ✅ Web search
- ✅ Multi-turn chat
- ✅ Full demo
- ✅ Config examples

### Tools
- ✅ Installation test
- ✅ Quick start scripts
- ✅ Environment template

## 🌟 Why This Framework?

| Feature | This Framework | Others |
|---------|---------------|---------|
| **Simplicity** | ✅ ~750 lines | ❌ Thousands |
| **Documentation** | ✅ 7 guides | ❌ Basic |
| **Examples** | ✅ 5+ working | ❌ Few |
| **Learning** | ✅ Tutorial included | ❌ None |
| **Architecture** | ✅ Well-designed | ❓ Varies |
| **Production patterns** | ✅ Yes | ❓ Maybe |

## 📝 Quick Reference

### CLI Commands
```bash
# Interactive mode
python -m gemini_agent.cli

# Single question
python -m gemini_agent.cli "Your question"

# With config
python -m gemini_agent.cli --config config.yaml

# Enable features
python -m gemini_agent.cli --enable-code-execution
python -m gemini_agent.cli --enable-web-search
```

### Python API
```python
from gemini_agent import create_agent

# Basic agent
agent = create_agent()

# With features
agent = create_agent(
    model="gemini-2.0-flash-exp",
    system_message="Custom prompt",
    enable_code_execution=True,
    enable_web_search=True,
)

# Stream responses
async for chunk in agent.chat("Hello"):
    print(chunk.content)

# Simple response
response = await agent.chat_simple("Hello")
```

## 🎊 Ready to Go!

You have everything you need:

✅ Working code
✅ Complete documentation
✅ Practical examples
✅ Learning materials
✅ Quick start guides

**Pick your starting point and dive in!**

---

## 📍 Important Links

- **Quick Setup** → [QUICKSTART.md](QUICKSTART.md)
- **Learning Path** → [TUTORIAL.md](TUTORIAL.md)
- **Full Reference** → [README.md](README.md)
- **All Docs** → [INDEX.md](INDEX.md)

---

**Let's build something amazing! 🚀🤖**
