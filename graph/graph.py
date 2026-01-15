import os
import subprocess
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain.messages import SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def run_command(cmd: str):
    """Executes a Windows CMD command."""
    ALLOWED_PREFIXES = (
        "python",
        "node",
        "npm",
        "dir",
        "mkdir",
        "cd",
        "type",
    )

    if not cmd.strip().startswith(ALLOWED_PREFIXES):
        return {"error": f"Command not allowed: {cmd}"}

    completed = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }

@tool
def write_file(path: str, content: str):
    """Writes code to a file inside chat_gpt/."""
    if not path.startswith("chat_gpt/"):
        return {"error": "All files must be inside chat_gpt/"}

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"status": "ok", "path": path}

@tool
def read_file(path: str):
    """Reads a file from chat_gpt/."""
    if not path.startswith("chat_gpt/"):
        return {"error": "Access denied"}

    with open(path, "r", encoding="utf-8") as f:
        return {"content": f.read()}


llm = init_chat_model(
    model_provider="openai",
    model="gpt-4o-mini",
)

llm_with_tools = llm.bind_tools(
    tools=[
        run_command,
        write_file,
        read_file,
    ]
)

# -------------------------
# Chain of Thought node
# -------------------------

def cot(state: State):
    """Chain of Thought reasoning before taking action."""
    cot_prompt = SystemMessage(content="""
Based on the user's request, think step by step about how to accomplish the task.

Break down the problem into:
1. What is the user asking for?
2. What steps are needed to complete this task?
3. What tools/commands will I need to use?
4. What's the correct order of operations?

Provide your reasoning clearly, then proceed to use the appropriate tools.
""")

    response = llm.invoke(
        [cot_prompt] + state["messages"]
    )

    return {"messages": [response]}

# -------------------------
# Chatbot node
# -------------------------

def chatbot(state: State):
    system_prompt = SystemMessage(content="""
You are an AI coding assistant running on Windows CMD.

IMPORTANT RULES:
- Shell is Windows CMD, NOT bash or zsh
- NEVER use Unix commands (-p, ls, rm -rf)
- Use Windows syntax only

TOOLS RULES:
- Write code → write_file
- Run code → run_command
- Never print code in chat
- Always use chat_gpt/ directory

If a command fails, read stderr and fix it.
""")

    response = llm_with_tools.invoke(
        [system_prompt] + state["messages"]
    )

    return {"messages": [response]}

# -------------------------
# Graph with CoT
# -------------------------

graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("cot", cot)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node(
    "tools",
    ToolNode([
        run_command,
        write_file,
        read_file,
    ])
)

# Define flow: START -> CoT -> Chatbot -> Tools (conditional) -> Chatbot -> END
graph_builder.add_edge(START, "cot")
graph_builder.add_edge("cot", "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# -------------------------
# Entry helper
# -------------------------

def create_chat_graph(checkpointer=None):
    return graph_builder.compile(checkpointer=checkpointer)