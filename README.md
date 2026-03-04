# 🎫 Ticket Agent

An intelligent support ticket agent powered by **LangGraph** and **Snowflake Cortex**. This agent automatically handles customer support inquiries by evaluating priority, retrieving relevant context using semantic search, and generating helpful responses.

## ✨ Features

- **Priority Classification** – Automatically classifies incoming messages as URGENT, HIGH, MEDIUM, or LOW priority
- **Semantic Context Retrieval** – Uses Snowflake Cortex Search to find relevant past tickets and knowledge base articles
- **AI-Powered Responses** – Generates helpful, context-aware support responses using LLMs
- **Ticket Management** – Creates new tickets or updates existing conversations
- **Conversation History** – Stores all messages for audit and continuity

## 🏗️ Architecture

The agent uses a LangGraph state machine with the following workflow:

```
┌─────────┐    ┌──────────────┐    ┌──────────┐    ┌──────────┐    ┌────────────────┐
│  START  │───▶│Load History  │───▶│ Priority │───▶│ Retrieve │───▶│    Generate    │
└─────────┘    └──────────────┘    └──────────┘    └──────────┘    └───────┬────────┘
                                                                            │
                                                               ┌────────────┴────────────┐
                                                               ▼                         ▼
                                                       ┌──────────────┐         ┌──────────────┐
                                                       │ Create Ticket│         │Update Ticket │
                                                       └──────┬───────┘         └──────┬───────┘
                                                              │                        │
                                                              └──────────┬─────────────┘
                                                                         ▼
                                                               ┌──────────────────┐
                                                               │ Store Agent Msg  │
                                                               └────────┬─────────┘
                                                                        ▼
                                                               ┌──────────────────┐
                                                               │Check for Resolve │
                                                               └────────┬─────────┘
                                                                        ▼
                                                                   ┌─────────┐
                                                                   │   END   │
                                                                   └─────────┘
```

### Nodes

| Node | Description |
|------|-------------|
| `load_history` | Loads past ticket messages |
| `priority` | Classifies the user message priority using an LLM |
| `retrieve` | Fetches relevant context from Snowflake Cortex Search |
| `generate` | Generates a support response based on priority and context |
| `create_ticket` | Creates a new ticket in the database |
| `update_ticket` | Adds a message to an existing ticket |
| `store_agent_message` | Persists the agent's response |
| `check_for_resolution` | Checks if the issue is resolved and updates ticket status |

## 📁 Project Structure

```
ticket_agent/
├── backend/
│   ├── agent.py                     # Main agent entry point
│   ├── db/
│   │   ├── snowflake_utils.py       # Snowflake session management utils
│   │   ├── sql_utils.py             # SQL execution helpers
│   │   ├── zen_repo.py              # Ticket repository operations
│   │   ├── csv/                     # CSV files for sample data
│   │   ├── tables/                  # SQL table definitions
│   │   ├── views/                   # SQL view definitions
│   │   └── cortex_search_services/  # SQL cortex definitions
│   ├── graph/
│   │   ├── graph.py                 # LangGraph workflow definition
│   │   ├── router.py                # Conditional routing logic
│   │   ├── state.py                 # State schema definition
│   │   └── nodes/                   # Individual graph nodes
│   └── llm/
│       └── model.py                 # LLM configuration
├── scripts/
│   ├── setup_db.py                  # Database setup script
│   └── chat_with_agent.py           # CLI chat interface
├── frontend/
│   ├── app.py                       # Streamlit app entry point
│   └── pages/                       # Streamlit app pages
├── requirements.txt
├── Makefile
└── .env.example
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Snowflake account with Cortex enabled
- Mistral API key (used in `backend/llm/model.py`, you can change the code to use another LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ticket_agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   make venv
   source venv/bin/activate
   ```

3. **Configure environment variables**
   
   Copy the example file and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

   Required variables:
   | Variable | Description |
   |----------|-------------|
   | `SNOWFLAKE_ACCOUNT` | Your Snowflake account identifier |
   | `SNOWFLAKE_USER` | Snowflake username |
   | `SNOWFLAKE_TOKEN` | Snowflake password/token |
   | `MISTRAL_API_KEY` | API key |
   | `SNOWFLAKE_WAREHOUSE` | Compute warehouse name |
   | `SNOWFLAKE_DATABASE` | Database containing your data |
   | `SNOWFLAKE_SCHEMA` | Schema name |
   | `SNOWFLAKE_CORTEX_SEARCH_SERVICE` | Cortex Search service name |

### Running the Agent

To test the agent through command line, run:

```bash
make run_agent
# or
PYTHONPATH=.:backend python scripts/chat_with_agent.py
```

### Running the Frontend

Start the ticketing system UI:

```bash
make app
# or
streamlit run frontend/app.py
```

## 🛠️ Technologies

- **[LangGraph](https://github.com/langchain-ai/langgraph)** – Stateful agent orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** – LLM integration
- **[Snowflake](https://www.snowflake.com)** – Data storage and processing
- **[Snowflake Cortex](https://www.snowflake.com/en/data-cloud/cortex/)** – Semantic search & LLM inference
## 📄 License
- **[Streamlit](https://streamlit.io/)** - App frontend