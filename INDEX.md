# 📚 Documentation Index

Welcome to the Gemini Simple Agent Framework! This index will help you find the right documentation for your needs.

## 🚀 Getting Started

**New to the framework? Start here:**

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡ (5 minutes)
   - Quick installation and setup
   - First commands to try
   - Common usage patterns

2. **[TUTORIAL.md](TUTORIAL.md)** 📖 (60 minutes)
   - Step-by-step learning guide
   - From basics to advanced features
   - Hands-on examples and exercises

3. **[README.md](README.md)** 📋 (Complete reference)
   - Full feature documentation
   - All command-line options
   - Configuration reference
   - Troubleshooting guide

## 🏗️ Understanding the System

**Want to understand how it works?**

4. **[ARCHITECTURE.md](ARCHITECTURE.md)** 🔧
   - System architecture diagrams
   - Component interaction flows
   - Data flow visualization
   - Extension points

5. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** 📊
   - Project overview
   - Design decisions
   - Comparison with other frameworks
   - What you can learn

## 📝 Configuration

**Setting up your agent:**

6. **[config.yaml](config.yaml)**
   - Default configuration example
   - Basic single-agent setup

7. **Example Configurations** in `examples/`:
   - `config_code_execution.yaml` - Python code execution
   - `config_web_search.yaml` - Web search capability
   - `config_full_tools.yaml` - All tools enabled

## 💻 Code Examples

**Learn by example:**

8. **[examples/simple_example.py](examples/simple_example.py)**
   - Basic agent usage
   - Streaming responses
   - Conversation flow

9. **[examples/code_execution_example.py](examples/code_execution_example.py)**
   - Using code execution
   - Solving problems with code

10. **[examples/web_search_example.py](examples/web_search_example.py)**
    - Web search integration
    - Real-time information retrieval

11. **[examples/multi_turn_example.py](examples/multi_turn_example.py)**
    - Multi-turn conversations
    - Context management

12. **[examples/full_demo.py](examples/full_demo.py)**
    - Comprehensive feature showcase
    - All capabilities demonstrated

## 🛠️ Setup and Testing

**Get up and running:**

13. **[requirements.txt](requirements.txt)**
    - Python dependencies
    - Required packages

14. **[setup.py](setup.py)**
    - Package installation
    - Console script entry points

15. **[test_setup.py](test_setup.py)**
    - Installation verification
    - Environment check
    - Basic functionality test

16. **Quick Start Scripts:**
    - `quickstart.bat` (Windows)
    - `quickstart.sh` (Unix/Linux/Mac)

## 📄 Legal and Environment

17. **[LICENSE](LICENSE)**
    - MIT License
    - Usage rights

18. **[.env.example](.env.example)**
    - Environment variable template
    - API key setup

19. **[.gitignore](.gitignore)**
    - Git ignore patterns

## 🗺️ Learning Paths

### Path 1: Quick Start (30 minutes)
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `python test_setup.py`
3. Try `python -m gemini_agent.cli`
4. Run `python examples/simple_example.py`

### Path 2: Comprehensive Learning (3 hours)
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Work through [TUTORIAL.md](TUTORIAL.md)
3. Run all example scripts
4. Read [ARCHITECTURE.md](ARCHITECTURE.md)
5. Build your own application

### Path 3: Advanced Development (Ongoing)
1. Understand [ARCHITECTURE.md](ARCHITECTURE.md)
2. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Study the source code in `gemini_agent/`
4. Extend and customize the framework

## 🎯 Quick References

### Common Tasks

**Install the framework:**
```bash
pip install -r requirements.txt
```

**Test your setup:**
```bash
python test_setup.py
```

**Interactive mode:**
```bash
python -m gemini_agent.cli
```

**Ask a question:**
```bash
python -m gemini_agent.cli "Your question here"
```

**Use a config file:**
```bash
python -m gemini_agent.cli --config config.yaml
```

**Run an example:**
```bash
python examples/simple_example.py
```

### Source Code Reference

**Core modules:**
- `gemini_agent/backend.py` - Gemini API wrapper
- `gemini_agent/agent.py` - Agent implementation
- `gemini_agent/cli.py` - Command-line interface
- `gemini_agent/config.py` - Configuration handling

## 📚 External Resources

**Related documentation:**
- [Google Gemini API Docs](https://ai.google.dev/)
- [Rich Library Docs](https://rich.readthedocs.io/)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)

## 🤔 Common Questions

**Q: Where do I start?**
A: Read [QUICKSTART.md](QUICKSTART.md) for a 5-minute introduction.

**Q: How do I enable code execution?**
A: See [examples/config_code_execution.yaml](examples/config_code_execution.yaml) or [TUTORIAL.md](TUTORIAL.md) Part 5.

**Q: How is this different from other frameworks?**
A: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) section "Comparison with other frameworks".

**Q: Can I use this in production?**
A: Yes, but consider adding error handling, rate limiting, and monitoring. See [ARCHITECTURE.md](ARCHITECTURE.md) for extension points.

**Q: How do I customize the system message?**
A: Edit `config.yaml` or use `--system-message` flag. See [README.md](README.md) for details.

**Q: What models are supported?**
A: All Google Gemini models. See [README.md](README.md) section "Available Models".

## 🆘 Getting Help

1. **Check the docs** - Use this index to find relevant documentation
2. **Run examples** - The `examples/` directory has working code
3. **Test setup** - Run `python test_setup.py` to verify installation
4. **Read errors** - Error messages include helpful hints
5. **Check source** - The code is well-documented with docstrings

## 📊 Documentation Overview

| Document | Purpose | Time | Audience |
|----------|---------|------|----------|
| QUICKSTART.md | Quick setup guide | 5 min | Everyone |
| TUTORIAL.md | Learning guide | 60 min | Learners |
| README.md | Complete reference | 20 min | All users |
| ARCHITECTURE.md | System design | 15 min | Developers |
| PROJECT_SUMMARY.md | Project overview | 10 min | Contributors |

## 🎓 Learning Objectives

After working through the documentation, you will be able to:

✅ Install and configure the framework
✅ Use the CLI for interactive and single-question modes
✅ Create and customize agents programmatically
✅ Enable and use code execution
✅ Enable and use web search
✅ Manage conversation history
✅ Load and create configuration files
✅ Extend the framework with new features
✅ Understand the architecture and design patterns

## 🚀 Next Steps

1. **Start learning**: Choose a learning path above
2. **Try examples**: Run the example scripts
3. **Build something**: Create your own agent application
4. **Share feedback**: Improve the framework
5. **Contribute**: Add features or examples

---

**Happy building with Gemini Agent Framework! 🤖**
