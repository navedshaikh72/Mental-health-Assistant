from fastapi import FastAPI, Request, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import requests
from collections import deque
import re
from datetime import datetime, timedelta
import json
import base64

# Import our new modules
from database import get_db, MoodEntry, ChatMessage, SelfHelpActivity
from emotion_detection import emotion_detector
from voice_processing import voice_processor
from self_help_toolkit import self_help_toolkit
from data_visualization import data_visualizer

app = FastAPI(title="Mental Health Assistant API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep the original chat history for backward compatibility
chat_history = deque(maxlen=100)

# Model details
API_Key = "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"
Model = "mistralai/mistral-7b-instruct"

SYSTEM_PROMPT = """
You are a compassionate, non-judgmental mental health assistant trained in Cognitive Behavioral Therapy (CBT).
Your goals:
- Listen empathetically to the user's concerns.
- Help reframe negative thoughts gently using CBT techniques.
- Never give medical advice or make diagnoses.
- Be calm, supportive, and safe in tone.
- Encourage users to seek professional help when appropriate.
- Provide practical coping strategies and self-care suggestions.
"""

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    voice_response: Optional[bool] = False

class MoodEntryRequest(BaseModel):
    mood_text: str
    mood_rating: int
    entry_type: Optional[str] = "text"

class SelfHelpRequest(BaseModel):
    activity_type: str  # "breathing", "affirmation", "cbt"
    activity_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    completion_rating: Optional[int] = None


@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user_message = request.message.strip()
    if not user_message:
        return JSONResponse(
            status_code=422,
            content={"error": "Missing or empty 'message' field in request body."}
        )

    # Detect emotions in user message
    emotions = emotion_detector.detect_emotions(user_message)
    dominant_emotion = emotion_detector.get_dominant_emotion(emotions)

    # Save user message to database
    user_chat = ChatMessage(
        role="user",
        content=user_message,
        detected_emotions=emotions,
        timestamp=datetime.utcnow()
    )
    db.add(user_chat)

    payload = {
        "model": Model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_Key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]:
            assistant_reply = result["choices"][0]["message"]["content"]
            
            # Save bot response to database
            bot_chat = ChatMessage(
                role="bot",
                content=assistant_reply,
                timestamp=datetime.utcnow()
            )
            db.add(bot_chat)
            db.commit()
            
            # Keep backward compatibility with chat_history
            chat_history.append({"role": "user", "content": user_message})
            chat_history.append({"role": "bot", "content": assistant_reply})
            
            response_data = {
                "response": assistant_reply,
                "detected_emotions": emotions,
                "dominant_emotion": dominant_emotion
            }
            
            # Add voice response if requested
            if request.voice_response:
                audio_base64 = voice_processor.text_to_speech(assistant_reply)
                if audio_base64:
                    response_data["audio"] = audio_base64
            
            return response_data
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "Model did not return any message."}
            )

    except requests.exceptions.RequestException as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error contacting model: {str(e)}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected error: {str(e)}"}
        )

# Weekly mental health summary endpoint
@app.get("/weekly_summary")
def get_weekly_summary(db: Session = Depends(get_db)):
    # Enhanced summary using database
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Get mood entries from database
    mood_entries = db.query(MoodEntry).filter(
        MoodEntry.date >= start_date,
        MoodEntry.date <= end_date
    ).all()
    
    if not mood_entries:
        # Fallback to old method for backward compatibility
        if not chat_history:
            return {"summary": "No chat history available for this week."}

        user_messages = [msg["content"] for msg in chat_history if msg["role"] == "user"]
        emotional_keywords = {
            "anxious": 0, "overwhelmed": 0, "sad": 0, "lonely": 0,
            "hopeful": 0, "calm": 0, "better": 0, "happy": 0
        }

        for message in user_messages:
            for word in emotional_keywords:
                if re.search(rf"\b{word}\b", message.lower()):
                    emotional_keywords[word] += 1

        common_emotions = sorted(emotional_keywords.items(), key=lambda x: x[1], reverse=True)
        summary_parts = []

        for emotion, count in common_emotions:
            if count > 0:
                summary_parts.append(f"{count}x '{emotion}'")

        if summary_parts:
            summary_text = "This week, you often expressed: " + ", ".join(summary_parts[:4]) + "."
        else:
            summary_text = "This week, your conversations were balanced without strong emotional words."

        return {"summary": summary_text}
    
    # Generate enhanced summary from database
    avg_mood = sum(entry.mood_rating for entry in mood_entries) / len(mood_entries)
    
    # Aggregate emotions
    emotion_totals = {}
    for entry in mood_entries:
        if entry.detected_emotions:
            emotions = entry.detected_emotions if isinstance(entry.detected_emotions, dict) else json.loads(entry.detected_emotions)
            for emotion, score in emotions.items():
                emotion_totals[emotion] = emotion_totals.get(emotion, 0) + score
    
    # Get top emotions
    top_emotions = sorted(emotion_totals.items(), key=lambda x: x[1], reverse=True)[:3]
    
    summary_text = f"This week, your average mood was {avg_mood:.1f}/10. "
    if top_emotions:
        emotion_names = [emotion[0] for emotion in top_emotions]
        summary_text += f"Your most prominent emotions were: {', '.join(emotion_names)}. "
    
    # Add personalized insights
    if avg_mood >= 7:
        summary_text += "You've been doing well this week! Keep up the positive momentum."
    elif avg_mood >= 5:
        summary_text += "Your mood has been moderate. Consider some self-care activities."
    else:
        summary_text += "It seems like you've had some challenging moments. Remember, it's okay to seek support."
    
    return {"summary": summary_text, "average_mood": avg_mood, "top_emotions": top_emotions}

# New endpoints for additional features
@app.post("/mood_entry")
async def create_mood_entry(request: MoodEntryRequest, db: Session = Depends(get_db)):
    """Create a new mood journal entry"""
    # Detect emotions in the mood text
    emotions = emotion_detector.detect_emotions(request.mood_text)
    
    # Create mood entry
    mood_entry = MoodEntry(
        mood_text=request.mood_text,
        mood_rating=request.mood_rating,
        detected_emotions=emotions,
        entry_type=request.entry_type,
        date=datetime.utcnow()
    )
    
    db.add(mood_entry)
    db.commit()
    db.refresh(mood_entry)
    
    # Generate personalized self-help recommendations
    dominant_emotion = emotion_detector.get_dominant_emotion(emotions)
    recommendations = self_help_toolkit.create_personalized_plan(request.mood_rating, dominant_emotion)
    
    return {
        "entry_id": mood_entry.id,
        "detected_emotions": emotions,
        "dominant_emotion": dominant_emotion,
        "recommendations": recommendations,
        "message": "Mood entry saved successfully!"
    }

@app.post("/mood-entry")
async def create_mood_entry_hyphenated(request: MoodEntryRequest, db: Session = Depends(get_db)):
    """Create mood entry with hyphenated URL"""
    return await create_mood_entry(request, db)

@app.post("/voice_to_text")
async def voice_to_text(audio: UploadFile = File(...)):
    """Convert uploaded audio to text"""
    try:
        audio_data = await audio.read()
        transcribed_text = voice_processor.process_audio_upload(audio_data, audio.filename.split('.')[-1])
        
        if transcribed_text:
            return {"text": transcribed_text}
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to transcribe audio"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing audio: {str(e)}"}
        )

@app.post("/text_to_speech")
async def text_to_speech(text: str = Form(...)):
    """Convert text to speech"""
    audio_base64 = voice_processor.text_to_speech(text)
    if audio_base64:
        return {"audio": audio_base64}
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to generate speech"}
        )

@app.get("/self_help/exercises")
async def get_self_help_exercises():
    """Get available self-help exercises"""
    return self_help_toolkit.get_all_exercise_names()

@app.get("/self_help/affirmation")
async def get_daily_affirmation():
    """Get a daily affirmation"""
    return {"affirmation": self_help_toolkit.get_daily_affirmation()}

@app.get("/self_help/breathing/{exercise_name}")
async def get_breathing_exercise(exercise_name: str):
    """Get a specific breathing exercise"""
    exercise = self_help_toolkit.get_breathing_exercise(exercise_name)
    return exercise

@app.get("/self_help/cbt/{exercise_name}")
async def get_cbt_exercise(exercise_name: str):
    """Get a specific CBT exercise"""
    exercise = self_help_toolkit.get_cbt_exercise(exercise_name)
    return exercise

@app.post("/self_help/complete")
async def complete_self_help_activity(request: SelfHelpRequest, db: Session = Depends(get_db)):
    """Record completion of a self-help activity"""
    activity = SelfHelpActivity(
        activity_type=request.activity_type,
        duration_seconds=request.duration_seconds,
        completion_rating=request.completion_rating,
        timestamp=datetime.utcnow()
    )
    
    db.add(activity)
    db.commit()
    
    return {"message": "Activity completion recorded!", "activity_id": activity.id}

@app.get("/visualizations/mood_trend")
async def get_mood_trend_chart(days: int = 30, db: Session = Depends(get_db)):
    """Get mood trend visualization"""
    chart_base64 = data_visualizer.create_mood_trend_chart(db, days)
    return {"chart": chart_base64, "type": "mood_trend"}

@app.get("/visualizations/weekly_heatmap")
async def get_weekly_heatmap(weeks: int = 12, db: Session = Depends(get_db)):
    """Get weekly mood heatmap"""
    chart_base64 = data_visualizer.create_weekly_mood_heatmap(db, weeks)
    return {"chart": chart_base64, "type": "weekly_heatmap"}

@app.get("/visualizations/comprehensive_report")
async def get_comprehensive_report(days: int = 30, db: Session = Depends(get_db)):
    """Get comprehensive visual report"""
    report = data_visualizer.generate_comprehensive_report(db, days)
    return report

@app.get("/mood_entries")
async def get_mood_entries(days: int = 30, db: Session = Depends(get_db)):
    """Get recent mood entries"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    entries = db.query(MoodEntry).filter(
        MoodEntry.date >= start_date,
        MoodEntry.date <= end_date
    ).order_by(MoodEntry.date.desc()).all()
    
    return [
        {
            "id": entry.id,
            "date": entry.date.isoformat(),
            "mood_text": entry.mood_text,
            "mood_rating": entry.mood_rating,
            "detected_emotions": entry.detected_emotions,
            "entry_type": entry.entry_type
        }
        for entry in entries
    ]

@app.get("/stats/overview")
async def get_stats_overview(db: Session = Depends(get_db)):
    """Get overview statistics"""
    # Count entries
    total_mood_entries = db.query(MoodEntry).count()
    total_chat_messages = db.query(ChatMessage).count()
    total_activities = db.query(SelfHelpActivity).count()
    
    # Recent mood average (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_moods = db.query(MoodEntry).filter(MoodEntry.date >= week_ago).all()
    recent_avg = sum(entry.mood_rating for entry in recent_moods) / len(recent_moods) if recent_moods else 0
    
    return {
        "total_mood_entries": total_mood_entries,
        "total_chat_messages": total_chat_messages,
        "total_self_help_activities": total_activities,
        "recent_average_mood": round(recent_avg, 1),
        "streak_days": len(recent_moods)  # Simplified streak calculation
    }

# Additional endpoints with hyphenated URLs for frontend compatibility
@app.get("/mood-entries")
async def get_mood_entries_hyphenated(limit: int = 10, db: Session = Depends(get_db)):
    """Get mood entries with hyphenated URL"""
    mood_entries = db.query(MoodEntry).order_by(MoodEntry.date.desc()).limit(limit).all()
    return [
        {
            "id": entry.id,
            "date": entry.date.isoformat(),
            "mood_rating": entry.mood_rating,
            "mood_text": entry.mood_text,
            "detected_emotions": entry.detected_emotions,
            "entry_type": entry.entry_type
        }
        for entry in mood_entries
    ]

@app.get("/self-help-recommendations")
async def get_self_help_recommendations():
    """Get self-help recommendations"""
    from self_help_toolkit import SelfHelpToolkit
    toolkit = SelfHelpToolkit()
    
    return {
        "breathing_exercises": toolkit.get_all_exercise_names()["breathing"],
        "cbt_exercises": toolkit.get_all_exercise_names()["cbt"],
        "random_breathing": toolkit.get_breathing_exercise(),
        "random_cbt": toolkit.get_cbt_exercise(),
        "affirmations": toolkit.get_multiple_affirmations(3)
    }

@app.get("/affirmations")
async def get_affirmations():
    """Get affirmations"""
    from self_help_toolkit import SelfHelpToolkit
    toolkit = SelfHelpToolkit()
    return {"affirmation": toolkit.get_daily_affirmation()}

@app.get("/analytics/mood-trends")
async def get_mood_trends_analytics(days: int = 30, db: Session = Depends(get_db)):
    """Get mood trends analytics"""
    from data_visualization import DataVisualizer
    visualizer = DataVisualizer()
    try:
        chart_data = visualizer.create_mood_trend_chart(db, days)
        return {"chart": chart_data, "type": "mood_trends", "days": days}
    except Exception as e:
        # Return simple data if visualization fails
        mood_entries = db.query(MoodEntry).order_by(MoodEntry.date.desc()).limit(days).all()
        if not mood_entries:
            return {"message": "No mood data available", "data": []}
        
        trend_data = [
            {
                "date": entry.date.isoformat(),
                "rating": entry.mood_rating,
                "emotion": list(entry.detected_emotions.keys())[0] if entry.detected_emotions else "neutral"
            }
            for entry in mood_entries
        ]
        return {"data": trend_data, "error": str(e)}

@app.get("/analytics/weekly-patterns")
async def get_weekly_patterns_analytics(db: Session = Depends(get_db)):
    """Get weekly patterns analytics"""
    from datetime import datetime, timedelta
    
    # Get all mood entries
    mood_entries = db.query(MoodEntry).all()
    
    if not mood_entries:
        return {
            "data": {
                "most_active_day": "No data",
                "avg_daily_entries": 0,
                "consistency_score": 0,
                "weekday_averages": {}
            },
            "message": "Not enough data for weekly patterns",
            "total_entries": 0
        }
    
    weekly_data = {}
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Initialize weekly data
    for day in weekdays:
        weekly_data[day] = {"ratings": [], "count": 0, "average": 0}
    
    # Process entries - use timestamp if date attribute doesn't exist
    for entry in mood_entries:
        try:
            # Try using date attribute first, fallback to timestamp
            entry_date = entry.date if hasattr(entry, 'date') and entry.date else entry.timestamp.date()
            week_day = entry_date.strftime("%A")
        except:
            # Fallback to timestamp weekday
            week_day = weekdays[entry.timestamp.weekday()]
            
        if week_day in weekly_data:
            if entry.mood_rating:
                weekly_data[week_day]["ratings"].append(entry.mood_rating)
            weekly_data[week_day]["count"] += 1
    
    # Calculate averages and statistics
    weekday_averages = {}
    for day in weekdays:
        if weekly_data[day]["ratings"]:
            weekly_data[day]["average"] = round(
                sum(weekly_data[day]["ratings"]) / len(weekly_data[day]["ratings"]), 1
            )
            weekday_averages[day] = weekly_data[day]["average"]
        else:
            weekday_averages[day] = 0
        # Remove raw ratings for cleaner response
        del weekly_data[day]["ratings"]
    
    # Find most active day
    most_active_day = max(weekdays, key=lambda day: weekly_data[day]["count"])
    avg_daily_entries = len(mood_entries) / 7
    
    # Calculate consistency score
    total_entries = len(mood_entries)
    ideal_per_day = total_entries / 7
    variance = sum((weekly_data[day]["count"] - ideal_per_day) ** 2 for day in weekdays) / 7
    consistency_score = max(0, 100 - (variance / ideal_per_day * 100)) if ideal_per_day > 0 else 0
    
    return {
        "data": {
            "most_active_day": most_active_day,
            "avg_daily_entries": round(avg_daily_entries, 1),
            "consistency_score": round(consistency_score, 1),
            "weekday_averages": weekday_averages,
            "weekly_breakdown": weekly_data
        },
        "total_entries": len(mood_entries),
        "days_with_data": len([day for day in weekly_data if weekly_data[day]["count"] > 0])
    }

@app.get("/weekly-summary")
async def get_weekly_summary_hyphenated(db: Session = Depends(get_db)):
    """Get weekly summary with hyphenated URL"""
    week_ago = datetime.now() - timedelta(days=7)
    
    # Get mood entries from last week
    mood_entries = db.query(MoodEntry).filter(MoodEntry.date >= week_ago.date()).all()
    
    if not mood_entries:
        return {
            "week_start": week_ago.strftime("%Y-%m-%d"),
            "week_end": datetime.now().strftime("%Y-%m-%d"),
            "average_mood": 0,
            "total_entries": 0,
            "mood_trend": "No data",
            "dominant_emotion": "No data",
            "insights": ["No mood data available for this week"]
        }
    
    # Calculate statistics
    avg_mood = sum(entry.mood_rating for entry in mood_entries) / len(mood_entries)
    
    # Extract emotions from detected_emotions JSON field
    emotions = []
    for entry in mood_entries:
        if entry.detected_emotions:
            if isinstance(entry.detected_emotions, list):
                emotions.extend(entry.detected_emotions)
            elif isinstance(entry.detected_emotions, dict):
                emotions.extend(entry.detected_emotions.keys())
            elif isinstance(entry.detected_emotions, str):
                emotions.append(entry.detected_emotions)
    
    # Find dominant emotion
    emotion_counts = {}
    for emotion in emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral"
    
    # Determine trend
    if len(mood_entries) >= 2:
        first_half = mood_entries[:len(mood_entries)//2]
        second_half = mood_entries[len(mood_entries)//2:]
        
        first_avg = sum(entry.mood_rating for entry in first_half) / len(first_half)
        second_avg = sum(entry.mood_rating for entry in second_half) / len(second_half)
        
        if second_avg > first_avg + 0.5:
            trend = "Improving"
        elif second_avg < first_avg - 0.5:
            trend = "Declining"
        else:
            trend = "Stable"
    else:
        trend = "Insufficient data"
    
    # Generate insights
    insights = []
    if avg_mood >= 7:
        insights.append("You had a great week! Your mood was consistently positive.")
    elif avg_mood >= 5:
        insights.append("You had a decent week with balanced emotions.")
    else:
        insights.append("This week was challenging. Consider self-care activities.")
    
    if dominant_emotion in ["joy", "optimism"]:
        insights.append(f"Your dominant emotion was {dominant_emotion} - keep up the positive energy!")
    elif dominant_emotion in ["anxiety", "sadness"]:
        insights.append(f"You experienced {dominant_emotion} frequently. Consider relaxation techniques.")
    
    return {
        "week_start": week_ago.strftime("%Y-%m-%d"),
        "week_end": datetime.now().strftime("%Y-%m-%d"),
        "average_mood": round(avg_mood, 1),
        "total_entries": len(mood_entries),
        "mood_trend": trend,
        "dominant_emotion": dominant_emotion,
        "insights": insights
    }

@app.get("/export-data")
async def export_data(db: Session = Depends(get_db)):
    """Export all user data"""
    mood_entries = db.query(MoodEntry).all()
    chat_messages = db.query(ChatMessage).all()
    activities = db.query(SelfHelpActivity).all()
    
    export_data = {
        "mood_entries": [
            {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "mood_rating": entry.mood_rating,
                "mood_text": entry.mood_text,
                "detected_emotions": entry.detected_emotions,
                "entry_type": entry.entry_type
            }
            for entry in mood_entries
        ],
        "chat_messages": [
            {
                "id": msg.id,
                "timestamp": msg.timestamp.isoformat(),
                "role": msg.role,
                "content": msg.content,
                "detected_emotions": msg.detected_emotions
            }
            for msg in chat_messages
        ],
        "self_help_activities": [
            {
                "id": activity.id,
                "timestamp": activity.timestamp.isoformat(),
                "activity_type": activity.activity_type,
                "duration_seconds": activity.duration_seconds,
                "completion_rating": activity.completion_rating
            }
            for activity in activities
        ],
        "export_timestamp": datetime.now().isoformat(),
        "total_records": len(mood_entries) + len(chat_messages) + len(activities)
    }
    
    return export_data

# Server startup
if __name__ == "__main__":
    import uvicorn
    print("Starting Mental Health Assistant API server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("API Documentation at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
