from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.config import settings

# Create SQLite engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for obtaining a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables in the database and run automatic lightweight column migrations"""
    Base.metadata.create_all(bind=engine)
    
    # Lightweight SQLite schema migration for newly added user_id column
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            # Check if user_id column exists in trip_plans
            res = conn.execute(text("PRAGMA table_info(trip_plans)")).fetchall()
            col_names = [r[1] for r in res]
            if "user_id" not in col_names:
                conn.execute(text("ALTER TABLE trip_plans ADD COLUMN user_id VARCHAR(36)"))
                conn.commit()
    except Exception as e:
        print("Database migration notice:", e)
