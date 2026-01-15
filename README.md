# VoiceCode - AI-Powered Coding Assistant with Voice Interface

An intelligent AI coding assistant that combines voice interaction, speech synthesis, and graph-based reasoning to help developers write, execute, and debug code through natural conversation. Powered by OpenAI's GPT models with LangGraph orchestration and MongoDB persistence.

## 📋 Project Overview

**VoiceCode** is a sophisticated voice-interactive AI coding assistant that demonstrates cutting-edge AI capabilities through a hands-on agent-driven experience. The assistant autonomously generates code artifacts (stored in `chat_gpt/`) to showcase its capabilities.

### Key Capabilities:
- **🎙️ Voice-First Interface**: Natural voice commands with real-time speech recognition and synthesized responses
- **🧠 Chain-of-Thought Reasoning**: Multi-step problem decomposition before code generation
- **⚙️ Code Execution**: Direct Windows CMD/PowerShell integration for running generated code
- **💾 File Manipulation**: Autonomous code generation and file management
- **🛡️ Safety & Validation**: Content filtering with toxic language detection and PII protection
- **🔄 Stateful Conversations**: MongoDB-backed persistence across sessions
- **📊 Web Artifacts**: Agent-generated HTML/CSS/JS demos showcasing capabilities

## 🏗️ Project Structure

```
voicecode/
├── docker-compose.yml          # MongoDB containerization
├── requirements.txt             # Python dependencies
├── graph/
│   ├── main.py                 # Voice interaction & agent orchestration
│   ├── graph.py                # LangGraph with Chain-of-Thought reasoning
│   └── __pycache__/            # Python cache files
├── chat_gpt/
│   ├── index.html              # Agent-generated: Portfolio landing page
│   ├── netflix_landing_page.html # Agent-generated: Netflix UI demo
│   ├── style.css               # Agent-generated: CSS styling
│   ├── script.js               # Agent-generated: JavaScript functionality
│   └── added.txt               # Agent notes/artifact tracker
└── __pycache__/                # Python cache files
```

📌 **Note**: Files in `chat_gpt/` are autonomously created by the AI agent to demonstrate code generation, web design, and file manipulation capabilities.

## ✨ Core Features Implemented

### 1. **Voice-Driven Interaction**
- Real-time speech recognition with ambient noise adjustment
- OpenAI TTS with customizable voice personality (cheerful, positive tone)
- Asynchronous audio streaming for responsive user experience

### 2. **AI Reasoning Engine**
- **Chain-of-Thought (CoT) Node**: Decomposes user requests into structured steps
- **Intelligent Chatbot Node**: Understands context and selects appropriate tools
- **Graph-Based Orchestration**: Optimal workflow routing (CoT → Chatbot → Tools → Response)

### 3. **Autonomous Code Generation & Execution**
- **write_file**: Agent creates HTML, CSS, JavaScript files autonomously
- **run_command**: Executes Windows commands for testing and validation
- **read_file**: Reads back generated code for verification and iteration
- **Whitelist Security**: Only safe commands allowed (python, node, npm, dir, mkdir, cd, type)

### 4. **Content Safety & Validation**
- **Toxic Language Detection**: Sentence-level filtering (threshold: 0.5)
- **PII Protection**: Identifies and masks sensitive data
  - IP Addresses
  - Aadhaar Numbers
  - Custom entity detection
- **Graceful Failure**: Skips harmful input and continues conversation

### 5. **Persistent State Management**
- **MongoDB Checkpointer**: Saves conversation state across sessions
- **Thread-Based Sessions**: Multiple independent conversations via thread IDs
- **Message History**: Complete audit trail of interactions

### 6. **Web Artifact Generation**
- **Portfolio Sites**: Full HTML/CSS/JS landing pages
- **Responsive Design**: Grid layouts and mobile-first styling
- **UI Frameworks**: Netflix-style dark mode interfaces
- **Interactive Elements**: DOM event handling and animations

### 7. **Error Handling & Recovery**
- Graceful exception management for guardrail violations
- Command execution error reporting with stdout/stderr
- File access violation prevention at tool level
- Automatic retry mechanisms for transient failures

## 🔧 Key Components

### 1. **graph/main.py** - Voice Agent Orchestrator
The main entry point managing voice-to-code interactions:

- **Speech Recognition**: Google Speech API with pause threshold tuning
- **Guardrail Processing**: Pre-validation of all user input
- **Graph Streaming**: Real-time event processing for responsive feedback
- **TTS Response**: Converts AI reasoning into spoken output
- **Persistence Layer**: MongoDB integration for chat history

**Demonstrated Capabilities**:
- Listens to natural language requests (e.g., "Create a portfolio website")
- Validates input against safety rules
- Streams the agent's chain-of-thought process
- Executes AI decisions (code generation, file creation)
- Speaks results back to user with emotional tone

### 2. **graph/graph.py** - AI Reasoning Graph with Tools
Advanced LangGraph implementation featuring three-tier reasoning:

**Chain-of-Thought Node**:
```
User Request → Break into steps → Plan execution → Reason about approach
```

**Chatbot Node**:
- Uses GPT-4o-mini for intelligent decision making
- Determines which tools to invoke
- Generates code/commands based on user intent

**Tool Execution Node**:
- `run_command(cmd)`: Execute Windows operations
  - Returns exit code, stdout, stderr
  - Whitelisted command prefixes for safety
- `write_file(path, content)`: Create/modify files in chat_gpt/
  - Sandboxed to chat_gpt/ directory only
  - Auto-creates parent directories
- `read_file(path)`: Access generated artifacts
  - Verify code quality before returning to user

**Graph Flow**:
```
START → Chain-of-Thought → Chatbot Node
           ↓
    (Tool Execution if needed)
           ↓
      Chatbot Node → END
```

### 3. **chat_gpt/** - Agent-Generated Artifacts
Showcase of autonomous code generation capabilities:

- **index.html**: Semantic HTML structure with navigation
- **netflix_landing_page.html**: Dark-mode streaming interface recreation
- **style.css**: Responsive grid layouts, modern typography, animations
- **script.js**: DOM manipulation and event handling

These files demonstrate the agent's ability to:
- Generate production-quality HTML/CSS
- Implement responsive design patterns
- Create themed UI components
- Write functional JavaScript

## 📦 Dependencies

Core packages used:

- **LangChain Ecosystem**: 
  - langchain (1.2.3)
  - langgraph (1.0.5)
  - langchain-openai (1.1.7)
  - langchain-mongodb (0.10.0)

- **Database**: 
  - pymongo (4.15.5)

- **AI/ML**:
  - openai (latest)
  - SpeechRecognition (3.14.2)
  - tiktoken (0.12.0)

- **Safety & Validation**:
  - guardrails-ai (for ToxicLanguage and PII detection)

- **Utilities**:
  - python-dotenv (1.2.1)
  - requests (2.32.5)
  - SQLAlchemy (2.0.45)
  - PyYAML (6.0.3)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Microphone hardware
- OpenAI API key

### Installation

1. **Clone/Navigate to project**:
   ```bash
   cd sts
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   ```bash
   docker-compose up -d
   ```

4. **Configure environment variables**:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_key_here
   MONGODB_URI=mongodb://admin:admin@localhost:27017
   ```

### Running the Application

**Start the voice chat**:
```bash
python graph/main.py
```

The application will:
1. Initialize MongoDB checkpointer
2. Create the conversation graph
3. Listen for voice input
4. Process through AI with guardrails
5. Respond with synthesized speech

## 🔐 Safety Features

- **Toxic Language Detection**: Threshold-based filtering (0.5)
- **PII Protection**: Identifies and masks sensitive data (IP addresses, Aadhaar numbers)
- **Command Whitelist**: Restricts executable commands to safe operations (python, node, npm, dir, mkdir, cd, type)
- **File Sandboxing**: All file operations limited to chat_gpt/ directory

## 🗄️ MongoDB Setup

Docker Compose configuration provides:
- **Service**: MongoDB latest image
- **Credentials**: admin/admin
- **Port**: 27017
- **Persistent Volume**: mongodb_data_v2

Used for:
- Conversation checkpointing
- Message history
- Thread state management

## 🎯 Use Cases

1. **Voice-Controlled Development**: Request code features naturally via voice
   - "Create a dark-themed landing page for Netflix"
   - "Generate a Python script that..."
   - "Build an HTML portfolio with multiple sections"

2. **Autonomous Code Generation**: Watch the agent generate, test, and refine code
   - Multi-file project creation
   - Responsive UI implementation
   - Script execution and debugging

3. **Hands-On AI Demonstration**: Showcase agent reasoning and decision-making
   - Chain-of-thought decomposition
   - Tool usage patterns
   - Real-time code generation

4. **Interactive Pair Programming**: Collaborate with an AI that:
   - Understands context
   - Reasons through problems
   - Executes and validates solutions
   - Explains its process

## 📝 Configuration

Key configuration in `graph/main.py`:
- **Thread ID**: "13" (can be modified for different conversation threads)
- **TTS Voice**: "coral" (cheerful and positive tone)
- **TTS Model**: gpt-4o-mini-tts
- **Pause Threshold**: 2 seconds
- **Toxic Content Threshold**: 0.5

## 🔄 Agent Workflow

```
🎤 Voice Input
    ↓
🔍 Speech Recognition (Google API)
    ↓
🛡️ Guardrail Validation (Toxic language, PII check)
    ↓
🧠 Chain-of-Thought Reasoning
    "Let me break down this request into steps..."
    ↓
🤖 Intelligent Decision Making
    "I need to create 3 files for this task"
    ↓
⚙️ Tool Execution (in order)
    • write_file → index.html
    • write_file → style.css
    • run_command → verify files
    ↓
💬 Response Generation
    "I've created a responsive landing page..."
    ↓
🔊 Text-to-Speech Output
    ↓
💾 MongoDB Persistence
    (Entire conversation saved)
```

## 🐛 Error Handling

- Guardrail violations trigger exception handling with skip to next input
- Command execution failures return error codes and messages
- File access violations prevented at tool level
- Async operation error management for audio playback

## 📚 Additional Notes

- The project uses LangGraph's prebuilt tool nodes for efficient tool management
- Conversation state is maintained through TypedDict with message annotations
- Audio processing uses LocalAudioPlayer for cross-platform compatibility
- MCP adapters enable advanced model context protocol integrations

## 🛠️ Future Enhancements

- **Multi-Modal Input**: Image analysis for UI design inspiration
- **Extended Tool Library**: Git operations, API calls, database queries
- **Code Review Agent**: Automated testing and security analysis
- **Version Control**: Track agent-generated code iterations
- **Web Dashboard**: Real-time visualization of agent reasoning
- **Custom Voice Models**: Fine-tuned for technical vocabulary
- **Plugin Architecture**: User-defined tools and integrations
- **Distributed Execution**: Cloud-based code execution for scalability

---

**Project Name**: VoiceCode  
**Type**: AI Coding Assistant with Voice Interface  
**Architecture**: Multi-agent LangGraph System  
**Status**: Active Development  
**Last Updated**: January 2026
