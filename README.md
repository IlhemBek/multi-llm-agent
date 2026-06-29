# 🤖 Multi-LLM AI Agent

An intelligent AI agent built with **LangChain**, **FastAPI**, and **Streamlit** that supports both **Claude (Anthropic)** and **Groq (LLaMA 3.3)** as LLM providers.

## ✨ Features

- 🔀 **Switch between LLMs** — Claude API or Groq, selectable at runtime
- 🌤 **Weather Tool** — Real-time weather data via OpenWeatherMap
- 🧮 **Calculator Tool** — Evaluate mathematical expressions
- 🔍 **Web Search Tool** — DuckDuckGo Instant Answers (no API key needed)
- 🖥 **Streamlit UI** — Clean chat interface with example queries
- ⚡ **FastAPI Backend** — REST API for programmatic access

## 🏗 Project Structure

```
multi_llm_agent/
├── agent/
│   ├── __init__.py
│   └── agent.py          # LangChain agent logic
├── tools/
│   ├── __init__.py
│   └── tools.py          # Weather, Calculator, Web Search tools
├── api/
│   └── main.py           # FastAPI REST API
├── streamlit_app.py      # Streamlit chat UI
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multi-llm-agent.git
cd multi-llm-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

> **Get your free API keys:**
> - Anthropic: https://console.anthropic.com
> - Groq: https://console.groq.com (free tier available)
> - OpenWeatherMap: https://openweathermap.org/api (free tier available)

### 4. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

### 5. Run the FastAPI server (optional)

```bash
uvicorn api.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

## 📡 API Usage

```bash
# Query with Claude
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in Paris?", "provider": "claude"}'

# Query with Groq
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 15% of 8500?", "provider": "groq"}'
```

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangChain |
| LLM (Option 1) | Claude Sonnet (Anthropic) |
| LLM (Option 2) | LLaMA 3.3 70B (Groq) |
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| Weather Data | OpenWeatherMap API |
| Web Search | DuckDuckGo API |

## 📄 License

MIT License — feel free to use and modify.

---

Built by [Ilhem B.](https://www.upwork.com/freelancers/~0175c416c324739a33) — AI Agent Developer
