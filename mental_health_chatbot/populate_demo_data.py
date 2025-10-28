#!/usr/bin/env python3
"""
Sample Data Populator for Mental Health Chatbot Demo
This script adds realistic sample data directly to the database
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database modules
from database import SessionLocal, MoodEntry, ChatMessage, SelfHelpActivity
from sqlalchemy.orm import Session

def create_sample_mood_entries(db: Session):
    """Create sample mood entries"""
    print("Creating sample mood entries...")
    
    sample_moods = [
        {"rating": 8, "text": "Had a great day at work, feeling accomplished", "emotion": "joy"},
        {"rating": 6, "text": "Feeling okay, bit tired from the week", "emotion": "neutral"},
        {"rating": 4, "text": "Stressed about upcoming deadlines", "emotion": "anxiety"},
        {"rating": 7, "text": "Good workout session, feeling energized", "emotion": "optimism"},
        {"rating": 5, "text": "Mixed day, some ups and downs", "emotion": "neutral"},
        {"rating": 9, "text": "Spent quality time with family", "emotion": "joy"},
        {"rating": 3, "text": "Feeling overwhelmed with responsibilities", "emotion": "sadness"},
        {"rating": 8, "text": "Completed a challenging project successfully", "emotion": "pride"},
        {"rating": 6, "text": "Regular day, nothing special", "emotion": "neutral"},
        {"rating": 7, "text": "Had a good conversation with a friend", "emotion": "joy"},
        {"rating": 4, "text": "Dealing with some personal issues", "emotion": "anxiety"},
        {"rating": 8, "text": "Beautiful weather, went for a long walk", "emotion": "joy"},
        {"rating": 5, "text": "Feeling uncertain about the future", "emotion": "fear"},
        {"rating": 7, "text": "Made progress on personal goals", "emotion": "optimism"},
        {"rating": 6, "text": "Quiet day, did some reading", "emotion": "neutral"},
        {"rating": 9, "text": "Celebrated a friend's birthday", "emotion": "joy"},
        {"rating": 4, "text": "Difficult conversation with colleague", "emotion": "anger"},
        {"rating": 7, "text": "Learned something new today", "emotion": "curiosity"},
        {"rating": 5, "text": "Feeling a bit lonely lately", "emotion": "sadness"},
        {"rating": 8, "text": "Productive morning, got lots done", "emotion": "pride"}
    ]
    
    for i, mood_data in enumerate(sample_moods):
        # Distribute entries over the past 30 days
        days_ago = random.randint(0, 29)
        entry_date = datetime.now() - timedelta(days=days_ago)
        
        mood_entry = MoodEntry(
            date=entry_date,
            mood_text=mood_data["text"],
            mood_rating=mood_data["rating"],
            detected_emotions={mood_data["emotion"]: 0.9},  # Simulate detection result
            entry_type="text"
        )
        
        db.add(mood_entry)
        print(f"✓ Added mood entry {i+1}: Rating {mood_data['rating']} - {mood_data['emotion']}")
    
    db.commit()
    print(f"✓ Created {len(sample_moods)} mood entries")

def create_sample_chat_messages(db: Session):
    """Create sample chat messages"""
    print("\nCreating sample chat messages...")
    
    sample_chats = [
        {"user": "I'm feeling anxious about my presentation tomorrow", "bot": "It's natural to feel anxious before presentations. Try some deep breathing exercises and visualize a successful outcome.", "emotion": "anxiety"},
        {"user": "How can I manage stress better?", "bot": "Here are some effective stress management techniques: regular exercise, meditation, proper sleep, and talking to friends or family.", "emotion": "anxiety"},
        {"user": "I had a great day today!", "bot": "That's wonderful! It's important to celebrate and acknowledge these positive moments. What made your day special?", "emotion": "joy"},
        {"user": "I'm feeling overwhelmed with work", "bot": "Feeling overwhelmed is tough. Try breaking tasks into smaller steps, prioritizing urgent items, and taking regular breaks.", "emotion": "sadness"},
        {"user": "Can you suggest some breathing exercises?", "bot": "Try the 4-7-8 technique: Inhale for 4 counts, hold for 7, exhale for 8. Repeat 3-4 times for immediate calm.", "emotion": "neutral"},
        {"user": "I accomplished my goals this week", "bot": "Congratulations! Achieving your goals is a great accomplishment. Take time to appreciate your hard work and progress.", "emotion": "pride"},
        {"user": "I'm worried about my family", "bot": "Family concerns can be really stressful. Consider having an open conversation with them or seeking support from friends.", "emotion": "fear"},
        {"user": "What are some ways to boost my mood?", "bot": "Try these mood boosters: listen to uplifting music, go for a walk, practice gratitude, connect with loved ones, or do something creative.", "emotion": "sadness"},
        {"user": "I feel grateful for my friends", "bot": "Gratitude is a powerful emotion! Having supportive friends is truly a blessing. Consider expressing your appreciation to them.", "emotion": "joy"},
        {"user": "How do I deal with negative thoughts?", "bot": "Try challenging negative thoughts by asking: Is this thought realistic? What would I tell a friend? Focus on facts rather than fears.", "emotion": "anxiety"}
    ]
    
    for i, chat_data in enumerate(sample_chats):
        # Distribute messages over the past 14 days
        days_ago = random.randint(0, 13)
        message_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 23))
        
        # Add user message
        user_message = ChatMessage(
            timestamp=message_time,
            role="user",
            content=chat_data["user"],
            detected_emotions={chat_data["emotion"]: 0.9}
        )
        db.add(user_message)
        
        # Add bot response (1 minute later)
        bot_message = ChatMessage(
            timestamp=message_time + timedelta(minutes=1),
            role="bot",
            content=chat_data["bot"],
            detected_emotions={}
        )
        db.add(bot_message)
        
        print(f"✓ Added chat exchange {i+1}: {chat_data['emotion']}")
    
    db.commit()
    print(f"✓ Created {len(sample_chats) * 2} chat messages")

def create_sample_activities(db: Session):
    """Create sample self-help activities"""
    print("\nCreating sample self-help activities...")
    
    sample_activities = [
        {"type": "breathing", "duration": 300, "rating": 4},  # 5 minutes
        {"type": "breathing", "duration": 240, "rating": 5},  # 4 minutes
        {"type": "meditation", "duration": 600, "rating": 3},  # 10 minutes
        {"type": "breathing", "duration": 180, "rating": 4},  # 3 minutes
        {"type": "affirmation", "duration": 120, "rating": 5},  # 2 minutes
        {"type": "meditation", "duration": 900, "rating": 2},  # 15 minutes
        {"type": "cbt", "duration": 1200, "rating": 4},  # 20 minutes
        {"type": "breathing", "duration": 300, "rating": 5},  # 5 minutes
        {"type": "meditation", "duration": 600, "rating": 4},  # 10 minutes
        {"type": "affirmation", "duration": 60, "rating": 3}   # 1 minute
    ]
    
    for i, activity_data in enumerate(sample_activities):
        # Distribute activities over the past 14 days
        days_ago = random.randint(0, 13)
        activity_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 23))
        
        activity = SelfHelpActivity(
            timestamp=activity_time,
            activity_type=activity_data["type"],
            duration_seconds=activity_data["duration"],
            completion_rating=activity_data["rating"]
        )
        
        db.add(activity)
        print(f"✓ Added activity {i+1}: {activity_data['type']} ({activity_data['duration']}s, rating: {activity_data['rating']})")
    
    db.commit()
    print(f"✓ Created {len(sample_activities)} self-help activities")

def check_existing_data(db: Session):
    """Check if data already exists"""
    mood_count = db.query(MoodEntry).count()
    chat_count = db.query(ChatMessage).count()
    activity_count = db.query(SelfHelpActivity).count()
    
    print(f"Current database contains:")
    print(f"  - {mood_count} mood entries")
    print(f"  - {chat_count} chat messages")
    print(f"  - {activity_count} self-help activities")
    
    return mood_count + chat_count + activity_count > 0

def main():
    """Main function to populate sample data"""
    print("Mental Health Chatbot - Direct Database Sample Data Populator")
    print("=" * 60)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check existing data
        has_data = check_existing_data(db)
        
        if has_data:
            response = input("\nDatabase already contains data. Do you want to add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled by user.")
                return
        
        print("\nAdding sample data...")
        
        # Create all sample data
        create_sample_mood_entries(db)
        create_sample_chat_messages(db)
        create_sample_activities(db)
        
        # Final summary
        print("\n" + "=" * 60)
        print("Sample data population completed!")
        
        final_mood_count = db.query(MoodEntry).count()
        final_chat_count = db.query(ChatMessage).count()
        final_activity_count = db.query(SelfHelpActivity).count()
        
        print(f"\nFinal database contains:")
        print(f"  - {final_mood_count} mood entries")
        print(f"  - {final_chat_count} chat messages")
        print(f"  - {final_activity_count} self-help activities")
        
        print("\nYou can now:")
        print("1. View analytics in your Flutter app")
        print("2. Check mood trends and patterns")
        print("3. See emotion distribution charts")
        print("4. Review self-help activity history")
        print("\nRefresh your analytics page to see the new data!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
