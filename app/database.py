from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# 📌 WHAT: Creates database engine using Unix socket
# 🎯 WHY: Postgres.app on Mac uses Unix socket at /tmp
#         instead of TCP/IP connection
# 💼 INTERVIEW: "I debugged a Mac-specific PostgreSQL
#         connection issue where psycopg2 needed Unix
#         socket path instead of TCP/IP"
engine = create_engine(
    "postgresql+psycopg2://kanish@/texttosql",
    connect_args={"host": "/tmp"}
)

def get_schema() -> str:
    """
    📌 WHAT: Reads all tables and columns from database
    🎯 WHY: LLM needs to know what tables/columns exist
            to generate correct SQL queries
    💼 INTERVIEW: "Instead of hardcoding schema, I fetch
            it dynamically so system works with ANY database"
    """
    schema_info = []
    
    with engine.connect() as conn:
        # Get all table names
        tables = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)).fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Get columns for each table
            columns = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = :table
            """), {"table": table_name}).fetchall()
            
            # Format table info
            col_info = ", ".join([f"{col[0]} ({col[1]})" 
                                 for col in columns])
            schema_info.append(
                f"Table: {table_name}\nColumns: {col_info}"
            )
    
    return "\n\n".join(schema_info)


# Test it
if __name__ == "__main__":
    print(get_schema())