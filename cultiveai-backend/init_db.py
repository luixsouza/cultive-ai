"""
Script para inicializar/atualizar o banco de dados.
Execute este script sempre que houver mudancas nos models.
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.base import Base
from app.db.session import engine

def init_db():
    """Create all tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
