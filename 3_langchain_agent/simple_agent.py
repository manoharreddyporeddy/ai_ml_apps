# ======================== LangChain + LangGraph Simple Agent ========================
# This code builds a minimal chatbot agent using LangChain and LangGraph libraries
# It uses a memory mechanism to remember the conversation and responds to user inputs.

# ------------------------------- What is LangChain? -------------------------------
# LangChain is a Python framework to build applications powered by LLMs (like GPT).
# It helps connect LLMs to tools, memory, APIs, files, databases, etc.
# Official docs: https://python.langchain.com/

# ------------------------------- What is LangGraph? -------------------------------
# LangGraph is an extension for LangChain that allows for building **stateful**
# and **multi-turn conversational agents** using a graph structure.
# It is ideal for memory, tool-calling, branching logic, and agent workflows.
# Docs: https://langchain-ai.github.io/langgraph/

# ========================== Step 1: Import required modules ==========================

import uuid  # To generate a unique ID for each conversation (thread)
from langchain_core.messages import HumanMessage  # Represents the user's input message
from langchain_openai import ChatOpenAI  # Wrapper to use OpenAI chat models
from langgraph.checkpoint.memory import MemorySaver  # Memory manager for LangGraph
from langgraph.prebuilt import create_react_agent  # Builds a ready-to-use ReAct agent
from langchain_core.tools import tool  # Used to define a tool the agent can use

# ====================== Step 2: Define the model you want to use ======================

# Use OpenAI's lightweight GPT-4.1 mini model
# (gpt-4.1-mini and gpt-4o-mini work well for simple agents, are cheaper and faster)
MODEL_NAME = "gpt-4.1-mini"

# ========================= Step 3: Define any custom tools ===========================


# A "tool" is a callable function that your AI agent can use.
# You can define tools like database lookups, calculations, etc.
@tool  # The @tool decorator registers this function as a usable tool for the agent
def echo_tool(text: str) -> str:
    """Echoes the input text."""
    return f"You said: {text}"


# ========================== Step 4: Setup memory and the model ========================

# MemorySaver is used by LangGraph to persist conversation memory between turns
memory = MemorySaver()

# Instantiate the LLM (ChatOpenAI) with your chosen model and temperature
# `temperature=0` makes the responses deterministic and less random
model = ChatOpenAI(model=MODEL_NAME, temperature=0)

# ======================= Step 5: Create the LangGraph ReAct agent =====================

# create_react_agent returns a complete agent using ReAct (Reasoning + Acting) pattern
# This agent can reason (think), use tools (act), and respond accordingly
app = create_react_agent(
    model=model,  # The LLM model to use
    tools=[echo_tool],  # List of tools the agent can access
    checkpointer=memory,  # Memory store to preserve chat history
)

# ======================= Step 6: Setup a unique thread for the user ===================

# A thread ID helps isolate memory for each user or session.
# You can later load the same thread_id to resume the chat
thread_id = uuid.uuid4()  # Random unique session ID

# LangGraph requires config with the thread_id under `configurable`
config = {"configurable": {"thread_id": thread_id}}

# ========================== Step 7: Send a message to the agent =======================

# Create a HumanMessage to simulate user input
message = HumanMessage(content="Hi, how are you?")

# Send the message into the agent and stream the result
# `stream_mode="values"` returns each stage of the conversation with responses
for event in app.stream({"messages": [message]}, config, stream_mode="values"):
    # Each `event` contains an updated message list
    # We print the last message (usually the AI's reply)
    event["messages"][-1].pretty_print()

#

# pip install --upgrade langchain langgraph langchain-openai

# Let me know if you'd like:
#     to extend this to multiple messages,
#     add summary memory,
#     call external APIs,
#     or log everything in a file or database.
