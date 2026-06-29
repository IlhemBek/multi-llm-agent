import os
import requests
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get current weather for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY not set in environment."
    
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            return f"Could not find weather for '{city}'. Please check the city name."
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        city_name = data["name"]
        country = data["sys"]["country"]
        
        return (
            f"Weather in {city_name}, {country}:\n"
            f"- Condition: {weather.capitalize()}\n"
            f"- Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"- Humidity: {humidity}%"
        )
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Example: '2 + 2', '15 * 4 / 3', 'sqrt(16)'."""
    import math
    
    allowed = {
        "abs": abs, "round": round,
        "sqrt": math.sqrt, "pow": math.pow,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "log": math.log, "log10": math.log10,
        "pi": math.pi, "e": math.e
    }
    
    try:
        expression_clean = expression.replace("^", "**")
        result = eval(expression_clean, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo Instant Answer API (no API key needed)."""
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        abstract = data.get("Abstract", "")
        answer = data.get("Answer", "")
        related = data.get("RelatedTopics", [])
        
        if answer:
            return f"Answer: {answer}"
        elif abstract:
            return f"Summary: {abstract}\nSource: {data.get('AbstractURL', '')}"
        elif related:
            results = []
            for item in related[:3]:
                if isinstance(item, dict) and "Text" in item:
                    results.append(f"- {item['Text']}")
            if results:
                return "Related results:\n" + "\n".join(results)
        
        return f"No direct answer found for '{query}'. Try rephrasing your question."
    except Exception as e:
        return f"Error during web search: {str(e)}"


TOOLS = [get_weather, calculate, web_search]
