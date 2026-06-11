from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from app.database import get_schema, engine
from app.validator import is_safe_query
from sqlalchemy import text
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL generator.
    
Here is the database schema:
{schema}

Rules:
- Generate only the SQL query, nothing else
- No explanations, no markdown, no backticks
- Only use tables and columns that exist in schema
- Always end query with semicolon
- Use = for exact string comparisons
"""),
    ("human", "{question}")
])

chain = prompt | llm

def generate_sql(question: str) -> str:
    schema = get_schema()
    response = chain.invoke({
        "schema": schema,
        "question": question
    })
    return response.content.strip()

def run_query(sql: str) -> list:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return result.fetchall()

def generate_sql_with_retry(question: str, max_retries: int = 3) -> dict:
    
    # Step 1 — Generate SQL
    sql = generate_sql(question)
    
    # Step 2 — Validate BEFORE executing
    is_safe, reason = is_safe_query(sql)
    if not is_safe:
        return {
            "success": False,
            "sql": sql,
            "results": [],
            "attempts": 0,
            "error": f"Blocked: {reason}"
        }
    
    # Step 3 — Execute with retry loop
    for attempt in range(max_retries):
        try:
            results = run_query(sql)
            return {
                "success": True,
                "sql": sql,
                "results": results,
                "attempts": attempt + 1
            }
        except Exception as error:
            print(f"❌ Attempt {attempt + 1} failed: {error}")
            if attempt < max_retries - 1:
                fix_prompt = f"""
                The following SQL query failed:
                {sql}
                Error message:
                {str(error)}
                Please fix the SQL query and return only the corrected SQL.
                """
                sql = llm.invoke(fix_prompt).content.strip()
                print(f"🔄 Retrying with fixed SQL: {sql}")
            else:
                return {
                    "success": False,
                    "sql": sql,
                    "results": [],
                    "attempts": max_retries,
                    "error": str(error)
                }

if __name__ == "__main__":
    question = "Show me all customers from New York"
    print(f"Question: {question}")
    result = generate_sql_with_retry(question)
    print(f"Success: {result['success']}")
    print(f"SQL: {result['sql']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Results: {result['results']}")