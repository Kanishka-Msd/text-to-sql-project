# 📌 WHAT: List of SQL keywords that can destroy data
# 🎯 WHY: Whitelist approach — we define exactly what
#         is dangerous rather than what is allowed
# 💼 INTERVIEW: "I implemented a blacklist of destructive
#         SQL keywords — this is the first line of defense
#         against accidental or malicious data loss"
DANGEROUS_KEYWORDS = [
    "DROP", "DELETE", "TRUNCATE", 
    "UPDATE", "INSERT", "ALTER",
    "CREATE", "REPLACE", "EXEC",
    "EXECUTE", "--", ";--", "/*"
]

def is_safe_query(sql: str) -> tuple[bool, str]:
    """
    📌 WHAT: Checks if SQL query is safe to execute
    🎯 WHY: Prevents destructive queries from reaching
            the database — critical for production safety
    💼 INTERVIEW: "Before executing any LLM-generated SQL,
            I validate it against a blacklist of dangerous
            keywords — this prevents SQL injection and
            accidental data destruction"
    """
    # Convert to uppercase for case-insensitive check
    sql_upper = sql.upper()
    
    for keyword in DANGEROUS_KEYWORDS:
        if keyword.upper() in sql_upper:
            return False, f"Dangerous keyword detected: {keyword}"
    
    # Must start with SELECT
    if not sql_upper.strip().startswith("SELECT"):
        return False, "Only SELECT queries are allowed"
    
    return True, "Query is safe"


def validate_and_explain(sql: str) -> dict:
    """
    📌 WHAT: Returns detailed validation result
    🎯 WHY: Gives clear feedback on WHY query was blocked
    💼 INTERVIEW: "I return structured validation results
            so the API can give meaningful error messages
            rather than generic failures"
    """
    is_safe, reason = is_safe_query(sql)
    
    return {
        "is_safe": is_safe,
        "reason": reason,
        "sql": sql
    }


# Test it
if __name__ == "__main__":
    test_queries = [
        "SELECT * FROM customers;",
        "DROP TABLE customers;",
        "DELETE FROM orders;",
        "SELECT * FROM customers; DROP TABLE customers;",
        "UPDATE customers SET city = 'London';"
    ]
    
    for query in test_queries:
        result = validate_and_explain(query)
        status = "✅ SAFE" if result["is_safe"] else "❌ BLOCKED"
        print(f"{status}: {query}")
        if not result["is_safe"]:
            print(f"   Reason: {result['reason']}")