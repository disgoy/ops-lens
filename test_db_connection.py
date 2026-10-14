

from sqlalchemy import text

from database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        print("Test query result:", result.scalar())
except Exception as error:
    print("Database connection failed.")
    print(f"Error type: {type(error).__name__}")
    print("Check your .env credentials and PostgreSQL service.")
