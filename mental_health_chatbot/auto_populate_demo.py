#!/usr/bin/env python3
"""
Auto Sample Data Populator for Mental Health Chatbot Demo
This script automatically adds sample data without user prompts
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database modules
from database import SessionLocal, MoodEntry, ChatMessage, SelfHelpActivity

def main():
    """Main function to populate sample data automatically"""
    print("Auto-populating sample data for demo...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data for clean demo
        print("Clearing existing data...")
        db.query(MoodEntry).delete()
        db.query(ChatMessage).delete()
        db.query(SelfHelpActivity).delete()
        db.commit()
        
        # Add mood entries
        print("Adding mood entries...")
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
            days_ago = random.randint(0, 29)
            entry_date = datetime.now() - timedelta(days=days_ago)
            
            mood_entry = MoodEntry(
                date=entry_date,
                mood_text=mood_data["text"],
                mood_rating=mood_data["rating"],
                detected_emotions={mood_data["emotion"]: 0.9},
                entry_type="text"
            )
            
            db.add(mood_entry)
            print(f"  ✓ Mood entry {i+1}: {mood_data['rating']}/10 - {mood_data['emotion']}")
        
        db.commit()
        
        # Add chat messages
        print("Adding chat messages...")
        sample_chats = [
            {"user": "I'm feeling anxious about my presentation", "emotion": "anxiety"},
            {"user": "How can I manage stress better?", "emotion": "anxiety"},
            {"user": "I had a great day today!", "emotion": "joy"},
            {"user": "I'm feeling overwhelmed with work", "emotion": "sadness"},
            {"user": "Can you suggest breathing exercises?", "emotion": "neutral"},
            {"user": "I accomplished my goals this week", "emotion": "pride"},
            {"user": "I'm worried about my family", "emotion": "fear"},
            {"user": "What are ways to boost my mood?", "emotion": "sadness"},
            {"user": "I feel grateful for my friends", "emotion": "joy"},
            {"user": "How do I deal with negative thoughts?", "emotion": "anxiety"}
        ]
        
        bot_responses = [
            "It's natural to feel anxious. Try deep breathing exercises.",
            "Regular exercise, meditation, and proper sleep help manage stress.",
            "That's wonderful! Celebrate and acknowledge positive moments.",
            "Try breaking tasks into smaller steps and taking regular breaks.",
            "Try the 4-7-8 technique: Inhale 4, hold 7, exhale 8 counts.",
            "Congratulations! Take time to appreciate your hard work.",
            "Family concerns are stressful. Consider open conversations.",
            "Listen to music, walk, practice gratitude, connect with loved ones.",
            "Gratitude is powerful! Express appreciation to your friends.",
            "Challenge thoughts: Is this realistic? Focus on facts, not fears."
        ]
        
        for i, chat_data in enumerate(sample_chats):
            days_ago = random.randint(0, 13)
            message_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 23))
            
            # User message
            user_message = ChatMessage(
                timestamp=message_time,
                role="user",
                content=chat_data["user"],
                detected_emotions={chat_data["emotion"]: 0.9}
            )
            db.add(user_message)
            
            # Bot response
            bot_message = ChatMessage(
                timestamp=message_time + timedelta(minutes=1),
                role="bot",
                content=bot_responses[i],
                detected_emotions={}
            )
            db.add(bot_message)
            
            print(f"  ✓ Chat exchange {i+1}: {chat_data['emotion']}")
        
        db.commit()
        
        # Add self-help activities
        print("Adding self-help activities...")
        sample_activities = [
            {"type": "breathing", "duration": 300, "rating": 4},
            {"type": "breathing", "duration": 240, "rating": 5},
            {"type": "meditation", "duration": 600, "rating": 3},
            {"type": "breathing", "duration": 180, "rating": 4},
            {"type": "affirmation", "duration": 120, "rating": 5},
            {"type": "meditation", "duration": 900, "rating": 2},
            {"type": "cbt", "duration": 1200, "rating": 4},
            {"type": "breathing", "duration": 300, "rating": 5},
            {"type": "meditation", "duration": 600, "rating": 4},
            {"type": "affirmation", "duration": 60, "rating": 3}
        ]
        
        for i, activity_data in enumerate(sample_activities):
            days_ago = random.randint(0, 13)
            activity_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 23))
            
            activity = SelfHelpActivity(
                timestamp=activity_time,
                activity_type=activity_data["type"],
                duration_seconds=activity_data["duration"],
                completion_rating=activity_data["rating"]
            )
            
            db.add(activity)
            print(f"  ✓ Activity {i+1}: {activity_data['type']} ({activity_data['duration']}s)")
        
        db.commit()
        
        # Final summary
        final_mood_count = db.query(MoodEntry).count()
        final_chat_count = db.query(ChatMessage).count()
        final_activity_count = db.query(SelfHelpActivity).count()
        
        print("\n" + "="*50)
        print("✅ DEMO DATA READY!")
        print(f"📊 Created {final_mood_count} mood entries")
        print(f"💬 Created {final_chat_count} chat messages")
        print(f"🧘 Created {final_activity_count} self-help activities")
        print("\n🎉 Your demo database is ready!")
        print("   Refresh your Flutter app to see the analytics!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
