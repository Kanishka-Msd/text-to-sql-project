from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.llm import generate_sql_with_retry

# 📌 WHAT: Creates FastAPI application instance
# 🎯 WHY: This is the entry point of our REST API
# 💼 INTERVIEW: "I used FastAPI because it's the
#         fastest Python API framework, has automatic
#         documentation, and native async support"
app = FastAPI(
    title="Text-to-SQL API",
    description="Convert plain English to SQL queries",
    version="1.0.0"
)

# 📌 WHAT: Defines the shape of incoming request
# 🎯 WHY: Pydantic validates data automatically —
#         if question is missing, API returns clear error
# 💼 INTERVIEW: "I used Pydantic models for request
#         validation — it ensures data integrity
#         before it reaches our LLM"
class QueryRequest(BaseModel):
    question: str

# 📌 WHAT: Defines the shape of our response
# 🎯 WHY: Consistent response structure makes it
#         easy for frontend to consume our API
# 💼 INTERVIEW: "I standardized the response schema
#         so every response has the same structure
#         regardless of success or failure"
class QueryResponse(BaseModel):
    question: str
    sql: str
    results: list
    attempts: int
    success: bool

# 📌 WHAT: Health check endpoint
# 🎯 WHY: Used by Docker/cloud to verify API is running
# 💼 INTERVIEW: "I added a health check endpoint —
#         standard practice in production systems
#         for load balancers and monitoring"
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 📌 WHAT: Main endpoint — converts English to SQL
# 🎯 WHY: Single responsibility — one endpoint
#         does one job cleanly
# 💼 INTERVIEW: "The /query endpoint receives natural
#         language, passes it through our agentic
#         loop, and returns structured results"
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    
    # Validate question is not empty
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    # Run through our self-correction loop
    result = generate_sql_with_retry(request.question)
    
    # If all retries failed
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Could not generate valid SQL after {result['attempts']} attempts"
        )
    
    return QueryResponse(
        question=request.question,
        sql=result["sql"],
        results=[list(row) for row in result["results"]],
        attempts=result["attempts"],
        success=result["success"]
    )