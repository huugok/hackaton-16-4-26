# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usaremos SQLite para el hackathon por su facilidad. Crea un archivo 'mindcheck.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./mindcheck.db"

# Equivalent a la cadena de conexión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal es el equivalente a tu sesión de DbContext
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de la cual heredarán nuestras entidades
Base = declarative_base()