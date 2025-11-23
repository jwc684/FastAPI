from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
# Defaults to PostgreSQL production if not set
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://fastapi_postgresql_txy0_user:vK7fp3b9bFPulxOWSrjrTjZRYqOM2Ah4@dpg-d4hduaumcj7s73bvcjs0-a.singapore-postgres.render.com/fastapi_postgresql_txy0"
)

# SQLite requires special connection args
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)


# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:qwer1234@127.0.0.1:3306/TodoApplicationDatabase'
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
#
# engine = = create_engine(
#   SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
