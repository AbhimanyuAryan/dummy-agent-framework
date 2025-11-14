# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  cli.py - Command-line interface                     │  │
│  │  - Interactive mode                                   │  │
│  │  - Single question mode                               │  │
│  │  - Rich terminal UI                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      Agent Layer                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  agent.py - Single Agent                             │  │
│  │  - Conversation history management                    │  │
│  │  - Session tracking                                   │  │
│  │  - Chat interface                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  backend.py - Gemini API Wrapper                     │  │
│  │  - Streaming responses                                │  │
│  │  - Tool integration (code exec, web search)           │  │
│  │  - Message formatting                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Google Gemini API                          │
│  - gemini-2.0-flash-exp                                      │
│  - gemini-2.5-pro                                            │
│  - Code execution                                            │
│  - Web search/grounding                                      │
└─────────────────────────────────────────────────────────────┘
```

## Component Interaction Flow

```
User Input
    │
    ▼
┌─────────────────┐
│   CLI Parser    │  Parse arguments, load config
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Config Loader   │  Load YAML, validate settings
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Agent Factory   │  Create agent with backend
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Agent       │  Manage conversation
│                 │
│  ┌───────────┐  │
│  │ History   │  │  Track messages
│  └───────────┘  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini Backend │  API communication
│                 │
│  ┌───────────┐  │
│  │ Streamer  │  │  Yield chunks
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Formatter │  │  Format messages
│  └───────────┘  │
└────────┬────────┘
         │
         ▼
   Gemini API
         │
         ▼
   Response Stream
         │
         ▼
     User Output
```

## Data Flow

### Streaming Response Flow

```
User Message
    │
    ▼
Agent.chat(message)
    │
    ├─ Append to history
    │
    ▼
Backend.chat_stream(messages)
    │
    ├─ Format messages for Gemini
    ├─ Build tools config
    ├─ Create API request
    │
    ▼
Gemini API (streaming)
    │
    ▼
async for chunk in response
    │
    ├─ Extract text
    ├─ Detect tool calls
    ├─ Yield StreamChunk
    │
    ▼
async for chunk in agent.chat()
    │
    ├─ Accumulate response
    ├─ Display to user
    │
    ▼
Complete Response
    │
    └─ Append to history
```

## Configuration Flow

```
config.yaml
    │
    ▼
Config Loader (config.py)
    │
    ├─ Parse YAML
    ├─ Extract agent config
    ├─ Extract backend config
    ├─ Extract UI config
    │
    ▼
Agent Factory
    │
    ├─ Create GeminiBackend
    │   ├─ API key
    │   ├─ Model name
    │   ├─ Enable tools
    │   └─ Generation params
    │
    ├─ Create Agent
    │   ├─ Backend instance
    │   ├─ System message
    │   └─ Session ID
    │
    ▼
Configured Agent
```

## File Organization

```
gemini_agent/
│
├── __init__.py          # Package exports
│   └── Exports: create_agent
│
├── backend.py           # Gemini API wrapper
│   ├── StreamChunk      # Data class for chunks
│   └── GeminiBackend    # Main backend class
│       ├── chat_stream()    # Streaming method
│       ├── chat()          # Non-streaming method
│       └── _format_messages()
│
├── agent.py             # Agent implementation
│   └── Agent            # Main agent class
│       ├── chat()          # Streaming chat
│       ├── chat_simple()   # Non-streaming chat
│       ├── reset()         # Clear history
│       └── get_status()    # Get agent info
│
├── cli.py              # Command-line interface
│   ├── interactive_mode()  # Chat loop
│   ├── single_question_mode()
│   └── main()             # Entry point
│
└── config.py           # Configuration handling
    ├── load_config()      # Load YAML
    ├── get_agent_config() # Extract agent settings
    └── get_ui_config()    # Extract UI settings
```

## Extension Points

### Adding New Features

1. **New Tool Integration**
   - Modify `GeminiBackend._build_tools_config()`
   - Add tool-specific parameters to config

2. **Custom Message Processing**
   - Override `Agent.chat()`
   - Add preprocessing/postprocessing hooks

3. **New Configuration Options**
   - Extend `config.yaml` schema
   - Update `get_agent_config()` parsing

4. **Alternative Interfaces**
   - Create new module alongside `cli.py`
   - Import from `gemini_agent` package
   - Use same Agent/Backend classes

### Example Extension: Adding a Web UI

```python
# web_ui.py
from fastapi import FastAPI
from gemini_agent import create_agent

app = FastAPI()
agent = create_agent(...)

@app.post("/chat")
async def chat(message: str):
    response = await agent.chat_simple(message)
    return {"response": response}
```

## Performance Characteristics

- **Latency**: ~1-3 seconds for first token (network dependent)
- **Throughput**: Streaming provides ~50-100 tokens/second
- **Memory**: ~50MB base + conversation history
- **Concurrency**: Supports async operations (multiple agents)

## Error Handling Strategy

```
User Input
    │
    ▼
┌─────────────────┐
│  Input Validation│
└────────┬────────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
         │ No
         ├──────► ValidationError
         │           │
         │ Yes       ▼
         ▼        Display Error
┌─────────────────┐
│  API Call       │
└────────┬────────┘
         │
    ┌────┴────┐
    │Success? │
    └────┬────┘
         │ No
         ├──────► APIError
         │           │
         │ Yes       ▼
         ▼        Retry/Display
┌─────────────────┐
│  Process Stream │
└────────┬────────┘
         │
    ┌────┴────┐
    │Success? │
    └────┬────┘
         │ No
         ├──────► StreamError
         │           │
         │ Yes       ▼
         ▼        Recover/Display
  Return Result
```

## Testing Strategy

1. **Unit Tests**: Test individual components
   - `test_backend.py` - Backend functionality
   - `test_agent.py` - Agent behavior
   - `test_config.py` - Config parsing

2. **Integration Tests**: Test component interaction
   - `test_cli.py` - CLI workflows
   - `test_e2e.py` - End-to-end scenarios

3. **Manual Testing**: Run example scripts
   - `test_setup.py` - Installation verification
   - `examples/*.py` - Feature demonstrations

---

This architecture provides:
- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add features without breaking existing code
- **Testability**: Components can be tested independently
- **Maintainability**: Clear separation of concerns
