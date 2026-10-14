
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load environment variables from the project's .env file.
load_dotenv()

# Build the connection URL safely, even if the password contains
# special characters such as @, /, or #.
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.environ["DB_NAME"],
)

# Engine manages database connectivity and connection pooling.
engine = create_engine(
    database_url,
    pool_pre_ping=True,
)

# Creates database sessions for individual units of work.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for our future database models.
class Base(DeclarativeBase):
    pass

