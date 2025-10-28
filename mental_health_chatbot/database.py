from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# Database setup
SQLITE_DATABASE_URL = "sqlite:///./mental_health.db"
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user")  # For future multi-user support
    date = Column(DateTime, default=datetime.utcnow)
    mood_text = Column(Text)
    mood_rating = Column(Integer)  # 1-10 scale
    detected_emotions = Column(JSON)  # Store emotion detection results
    entry_type = Column(String, default="text")  # "text" or "voice"
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user")
    timestamp = Column(DateTime, default=datetime.utcnow)
    role = Column(String)  # "user" or "bot"
    content = Column(Text)
    detected_emotions = Column(JSON)
    
class SelfHelpActivity(Base):
    __tablename__ = "self_help_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user")
    activity_type = Column(String)  # "breathing", "affirmation", "cbt"
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer)
    completion_rating = Column(Integer)  # 1-5 how helpful it was

# Create tables
Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
