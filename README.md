# 🧠 Text-to-SQL AI System

> Convert plain English questions into SQL queries using LangChain, Groq, and PostgreSQL — with an agentic self-correction loop for production-grade accuracy.

---

## 🎯 What It Does

This system allows **non-technical users** to query any PostgreSQL database using plain English — completely eliminating SQL dependency.

**Example:**
```
Input:  "Show me all customers from New York"
Output: SELECT * FROM customers WHERE city = 'New York';
Result: [Alice Johnson, Carol White]
```

---

## 🏗️ System Architecture

```
User Question
     ↓
FastAPI /query endpoint
     ↓
Fetch Live Schema (information_schema)
     ↓
Build Context-Aware Prompt (schema + question)
     ↓
Groq LLM (Llama 3.3 70B) → Generate SQL
     ↓
Security Validator (dangerous keywords check)
     ↓
Execute SQL on PostgreSQL
     ↓
Error? → Send error to LLM → Auto-Retry (max 3x)
     ↓
Return Structured JSON Response
```

---

## ⚙️ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Schema-Aware Prompting** | Dynamically reads live database schema at runtime |
| 🤖 **LLM SQL Generation** | Uses Groq's Llama 3.3 70B for fast, accurate SQL |
| 🔄 **Agentic Self-Correction** | Auto-retries up to 3 times on failure with error context |
| 🔒 **Security Validation** | Blocks dangerous keywords before execution |
| 🚀 **REST API** | Production-ready FastAPI with auto-generated docs |
| 🐳 **Dockerized** | Fully containerized and published on Docker Hub |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Groq API (Llama 3.3 70B) |
| **Orchestration** | LangChain |
| **API Framework** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Containerization** | Docker |
| **Deployment** | Docker Hub |

---

## 📁 Project Structure

```
text-to-sql-project/
├── app/
│   ├── main.py          # FastAPI routes and endpoints
│   ├── llm.py           # LangChain + Groq SQL generation
│   ├── database.py      # PostgreSQL connection + schema reading
│   └── validator.py     # SQL injection prevention
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL
- Groq API Key ([console.groq.com](https://console.groq.com))
- Docker (optional)

### 1. Clone The Repository
```bash
git clone https://github.com/Kanishka-Msd/text-to-sql-project.git
cd text-to-sql-project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user@localhost:5432/dbname
```

### 5. Run The API
```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

API will be live at: `http://localhost:8000`

---

## 🐳 Run With Docker

```bash
# Pull from Docker Hub
docker pull kanishka76/text-to-sql-app:latest

# Run the container
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  -e DATABASE_URL=your_db_url \
  kanishka76/text-to-sql-app:latest
```

---

## 📡 API Reference

### Health Check
```
GET /health
```
```json
{"status": "healthy"}
```

### Query Endpoint
```
POST /query
```

**Request:**
```json
{
  "question": "Show me all customers from New York"
}
```

**Response:**
```json
{
  "question": "Show me all customers from New York",
  "sql": "SELECT * FROM customers WHERE city = 'New York';",
  "results": [
    [1, "Alice Johnson", "alice@email.com", "New York"],
    [3, "Carol White", "carol@email.com", "New York"]
  ],
  "attempts": 1,
  "success": true
}
```

### Interactive API Docs
Visit `http://localhost:8000/docs` for Swagger UI

---

## 🔒 Security

The system includes a multi-layer security approach:

- **Keyword Blacklist** — Blocks DROP, DELETE, TRUNCATE, UPDATE, ALTER, INSERT
- **Query Type Enforcement** — Only SELECT queries are allowed
- **Pre-execution Validation** — Dangerous queries never reach the database
- **Environment Variables** — API keys never hardcoded in source code

---

## 🔄 Self-Correction Loop

```
Generate SQL
     ↓
Execute Query
     ↓
Success? ──YES──→ Return Results
     │
    NO
     ↓
Capture Error Message
     ↓
Send Error + Failed SQL to LLM
     ↓
LLM Generates Fixed SQL
     ↓
Retry (max 3 attempts)
```

---

## 🗄️ Sample Database Schema

```sql
customers   → id, name, email, city, created_at
products    → id, name, category, price, stock
orders      → id, customer_id, total_amount, status, order_date
order_items → id, order_id, product_id, quantity, price
```

---

## 🧪 Example Queries

| Plain English | Generated SQL |
|--------------|---------------|
| "Show all customers" | `SELECT * FROM customers;` |
| "Customers from New York" | `SELECT * FROM customers WHERE city = 'New York';` |
| "Products over $500" | `SELECT * FROM products WHERE price > 500;` |
| "Completed orders" | `SELECT * FROM orders WHERE status = 'completed';` |

---

## 🔮 Future Improvements

- **RAG Extension** — Vector embeddings for large schemas (25+ tables)
- **Query Caching** — Redis cache for repeated queries
- **Async Support** — Concurrent query handling
- **Multi-database** — Support MySQL, SQLite, Snowflake

---

## 👨‍💻 Author

**Kanishka**
- GitHub: [@Kanishka-Msd](https://github.com/Kanishka-Msd)
- Docker Hub: [kanishka76](https://hub.docker.com/u/kanishka76)

---

## 📄 License

MIT License — feel free to use this project for learning and portfolio purposes.