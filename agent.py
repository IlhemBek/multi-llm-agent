import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from tools import TOOLS


SYSTEM_PROMPT = """You are a helpful AI assistant with access to the following tools:

1. **get_weather**: Get real-time weather for any city
2. **calculate**: Evaluate mathematical expressions
3. **web_search**: Search the web for information

Always use the appropriate tool when the user's question requires it.
Be concise, accurate, and friendly in your responses.
"""


def get_llm(provider: str = "claude", model: str = None):
    """Initialize LLM based on provider choice."""
    if provider == "claude":
        model = model or "claude-sonnet-4-6"
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment.")
        return ChatAnthropic(model=model, anthropic_api_key=api_key, temperature=0)
    
    elif provider == "groq":
        model = model or "llama-3.3-70b-versatile"
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment.")
        return ChatGroq(model=model, groq_api_key=api_key, temperature=0)
    
    else:
        raise ValueError(f"Unknown provider: {provider}. Choose 'claude' or 'groq'.")


def build_agent(provider: str = "claude", model: str = None) -> AgentExecutor:
    """Build and return a LangChain agent with tools."""
    llm = get_llm(provider, model)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )


def run_agent(query: str, provider: str = "claude", model: str = None) -> dict:
    """Run agent with a query and return result."""
    try:
        agent_executor = build_agent(provider, model)
        result = agent_executor.invoke({"input": query})
        return {
            "success": True,
            "provider": provider,
            "query": query,
            "response": result.get("output", "No response generated.")
        }
    except Exception as e:
        return {
            "success": False,
            "provider": provider,
            "query": query,
            "error": str(e)
        }
