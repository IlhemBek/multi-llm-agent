import os
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from tools import TOOLS

def get_llm(provider="groq", model=None):
    if provider == "claude":
        model = model or "claude-haiku-4-5-20251001"
        return ChatAnthropic(model=model, anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"), temperature=0)
    elif provider == "groq":
        model = model or "llama-3.3-70b-versatile"
        return ChatGroq(model=model, groq_api_key=os.getenv("GROQ_API_KEY"), temperature=0)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def run_agent(query, provider="groq", model=None):
    try:
        llm = get_llm(provider, model)
        llm_with_tools = llm.bind_tools(TOOLS)
        messages = [{"role": "user", "content": query}]
        response = llm_with_tools.invoke(messages)
        
        if response.tool_calls:
            tool_map = {t.name: t for t in TOOLS}
            messages.append(response)
            for tool_call in response.tool_calls:
                tool = tool_map.get(tool_call["name"])
                if tool:
                    result = tool.invoke(tool_call["args"])
                    messages.append({
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool_call["id"]
                    })
            final = llm_with_tools.invoke(messages)
            return {"success": True, "provider": provider, "query": query, "response": final.content}
        
        return {"success": True, "provider": provider, "query": query, "response": response.content}
    except Exception as e:
        return {"success": False, "provider": provider, "query": query, "error": str(e)}

def build_agent(provider="groq", model=None):
    return get_llm(provider, model)
