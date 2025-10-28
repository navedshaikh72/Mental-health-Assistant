#!/usr/bin/env python3
"""
Sample Data Populator for Mental Health Chatbot Demo
This script adds realistic sample data to demonstrate all features
"""

import requests
import json
from datetime import datetime, timedelta
import random
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Sample data sets
SAMPLE_MOODS = [
    {"rating": 8, "notes": "Had a great day at work, feeling accomplished", "emotion": "joy"},
    {"rating": 6, "notes": "Feeling okay, bit tired from the week", "emotion": "neutral"},
    {"rating": 4, "notes": "Stressed about upcoming deadlines", "emotion": "anxiety"},
    {"rating": 7, "notes": "Good workout session, feeling energized", "emotion": "optimism"},
    {"rating": 5, "notes": "Mixed day, some ups and downs", "emotion": "neutral"},
    {"rating": 9, "notes": "Spent quality time with family", "emotion": "joy"},
    {"rating": 3, "notes": "Feeling overwhelmed with responsibilities", "emotion": "sadness"},
    {"rating": 8, "notes": "Completed a challenging project successfully", "emotion": "pride"},
    {"rating": 6, "notes": "Regular day, nothing special", "emotion": "neutral"},
    {"rating": 7, "notes": "Had a good conversation with a friend", "emotion": "joy"},
    {"rating": 4, "notes": "Dealing with some personal issues", "emotion": "anxiety"},
    {"rating": 8, "notes": "Beautiful weather, went for a long walk", "emotion": "joy"},
    {"rating": 5, "notes": "Feeling uncertain about the future", "emotion": "fear"},
    {"rating": 7, "notes": "Made progress on personal goals", "emotion": "optimism"},
    {"rating": 6, "notes": "Quiet day, did some reading", "emotion": "neutral"},
    {"rating": 9, "notes": "Celebrated a friend's birthday", "emotion": "joy"},
    {"rating": 4, "notes": "Difficult conversation with colleague", "emotion": "anger"},
    {"rating": 7, "notes": "Learned something new today", "emotion": "curiosity"},
    {"rating": 5, "notes": "Feeling a bit lonely lately", "emotion": "sadness"},
    {"rating": 8, "notes": "Productive morning, got lots done", "emotion": "pride"}
]

SAMPLE_CHAT_MESSAGES = [
    {"user": "I'm feeling anxious about my presentation tomorrow", "emotion": "anxiety"},
    {"user": "How can I manage stress better?", "emotion": "anxiety"},
    {"user": "I had a great day today!", "emotion": "joy"},
    {"user": "I'm feeling overwhelmed with work", "emotion": "sadness"},
    {"user": "Can you suggest some breathing exercises?", "emotion": "neutral"},
    {"user": "I accomplished my goals this week", "emotion": "pride"},
    {"user": "I'm worried about my family", "emotion": "fear"},
    {"user": "What are some ways to boost my mood?", "emotion": "sadness"},
    {"user": "I feel grateful for my friends", "emotion": "joy"},
    {"user": "How do I deal with negative thoughts?", "emotion": "anxiety"},
    {"user": "I'm excited about my vacation", "emotion": "joy"},
    {"user": "I feel stuck in my career", "emotion": "sadness"},
    {"user": "Can you help me with sleep issues?", "emotion": "anxiety"},
    {"user": "I'm proud of how far I've come", "emotion": "pride"},
    {"user": "I need help with time management", "emotion": "anxiety"}
]

SAMPLE_ACTIVITIES = [
    {"type": "breathing", "name": "Box Breathing", "completed": True},
    {"type": "cbt", "name": "Thought Challenging", "completed": True},
    {"type": "meditation", "name": "Mindfulness Session", "completed": False},
    {"type": "breathing", "name": "4-7-8 Breathing", "completed": True},
    {"type": "journaling", "name": "Gratitude Journal", "completed": True},
    {"type": "exercise", "name": "Progressive Muscle Relaxation", "completed": False},
    {"type": "cbt", "name": "Behavioral Activation", "completed": True},
    {"type": "breathing", "name": "Belly Breathing", "completed": True},
    {"type": "meditation", "name": "Body Scan", "completed": True},
    {"type": "journaling", "name": "Mood Tracking", "completed": True}
]

def add_mood_entries():
    """Add sample mood entries over the past 30 days"""
    print("Adding sample mood entries...")
    
    for i, mood_data in enumerate(SAMPLE_MOODS):
        # Distribute entries over the past 30 days
        days_ago = random.randint(0, 29)
        entry_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        payload = {
            "date": entry_date,
            "mood_rating": mood_data["rating"],
            "notes": mood_data["notes"]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/mood_entry", json=payload)
            if response.status_code == 200:
                print(f"✓ Added mood entry {i+1}: Rating {mood_data['rating']}")
            else:
                print(f"✗ Failed to add mood entry {i+1}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error adding mood entry {i+1}: {str(e)}")
        
        time.sleep(0.1)  # Small delay to avoid overwhelming the server

def add_chat_messages():
    """Add sample chat messages"""
    print("\nAdding sample chat messages...")
    
    for i, chat_data in enumerate(SAMPLE_CHAT_MESSAGES):
        payload = {"message": chat_data["user"]}
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            if response.status_code == 200:
                print(f"✓ Added chat message {i+1}")
            else:
                print(f"✗ Failed to add chat message {i+1}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error adding chat message {i+1}: {str(e)}")
        
        time.sleep(0.2)  # Small delay for chat processing

def add_self_help_activities():
    """Add sample self-help activities"""
    print("\nAdding sample self-help activities...")
    
    for i, activity_data in enumerate(SAMPLE_ACTIVITIES):
        # Distribute activities over the past 14 days
        days_ago = random.randint(0, 13)
        activity_date = datetime.now() - timedelta(days=days_ago)
        
        payload = {
            "activity_type": activity_data["type"],
            "activity_name": activity_data["name"],
            "completed": activity_data["completed"],
            "notes": f"Sample {activity_data['type']} activity for demo"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/self_help/complete", json=payload)
            if response.status_code == 200:
                print(f"✓ Added activity {i+1}: {activity_data['name']}")
            else:
                print(f"✗ Failed to add activity {i+1}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error adding activity {i+1}: {str(e)}")
        
        time.sleep(0.1)

def test_api_connection():
    """Test if the API is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/stats/overview")
        if response.status_code == 200:
            print("✓ API connection successful")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to API: {str(e)}")
        return False

def main():
    """Main function to populate all sample data"""
    print("Mental Health Chatbot - Sample Data Populator")
    print("=" * 50)
    
    # Test API connection first
    if not test_api_connection():
        print("\nPlease make sure the backend server is running on http://127.0.0.1:8000")
        return
    
    print("\nStarting data population...")
    
    # Add all sample data
    add_mood_entries()
    add_chat_messages()
    add_self_help_activities()
    
    print("\n" + "=" * 50)
    print("Sample data population completed!")
    print("\nYou can now:")
    print("1. View analytics in your Flutter app")
    print("2. Check mood trends and patterns")
    print("3. See emotion distribution charts")
    print("4. Review self-help activity history")
    print("\nRefresh your analytics page to see the new data!")

if __name__ == "__main__":
    main()
