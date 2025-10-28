from typing import Dict, List
import random
from datetime import datetime

class SelfHelpToolkit:
    def __init__(self):
        self.breathing_exercises = [
            {
                "name": "4-7-8 Breathing",
                "instructions": "Inhale for 4 counts, hold for 7 counts, exhale for 8 counts. Repeat 4 times.",
                "duration": 120,  # seconds
                "steps": [
                    "Find a comfortable position and close your eyes",
                    "Place your tongue against the roof of your mouth behind your front teeth",
                    "Exhale completely through your mouth",
                    "Inhale through your nose for 4 counts",
                    "Hold your breath for 7 counts",
                    "Exhale through your mouth for 8 counts",
                    "Repeat this cycle 3 more times"
                ]
            },
            {
                "name": "Box Breathing",
                "instructions": "Inhale for 4, hold for 4, exhale for 4, hold for 4. Repeat for 5 minutes.",
                "duration": 300,
                "steps": [
                    "Sit comfortably with your back straight",
                    "Exhale all air from your lungs",
                    "Inhale through your nose for 4 counts",
                    "Hold your breath for 4 counts",
                    "Exhale through your mouth for 4 counts",
                    "Hold empty for 4 counts",
                    "Repeat this pattern for 5 minutes"
                ]
            },
            {
                "name": "Progressive Muscle Relaxation",
                "instructions": "Tense and relax each muscle group, starting from your toes.",
                "duration": 900,  # 15 minutes
                "steps": [
                    "Lie down comfortably",
                    "Start with your toes - tense for 5 seconds, then relax",
                    "Move to your calves - tense and relax",
                    "Continue with thighs, abdomen, hands, arms, shoulders",
                    "Finish with your face muscles",
                    "Breathe deeply throughout the exercise"
                ]
            }
        ]
        
        self.affirmations = [
            "I am worthy of love and respect.",
            "I have the strength to overcome any challenge.",
            "I choose peace and calm in this moment.",
            "I am grateful for all the good things in my life.",
            "I trust in my ability to make good decisions.",
            "I am becoming the best version of myself.",
            "I deserve happiness and joy.",
            "I am resilient and can handle whatever comes my way.",
            "I choose to focus on what I can control.",
            "I am enough, just as I am.",
            "I forgive myself for past mistakes and learn from them.",
            "I attract positive energy and opportunities.",
            "I am capable of creating positive change in my life.",
            "I choose to see the good in every situation.",
            "I am surrounded by love and support."
        ]
        
        self.cbt_exercises = [
            {
                "name": "Thought Record",
                "description": "Identify and challenge negative thoughts",
                "steps": [
                    "What situation triggered this feeling?",
                    "What thoughts went through your mind?",
                    "What emotions did you feel (0-10 intensity)?",
                    "What evidence supports this thought?",
                    "What evidence contradicts this thought?",
                    "What would you tell a friend in this situation?",
                    "What's a more balanced way to think about this?"
                ]
            },
            {
                "name": "Gratitude Practice",
                "description": "Focus on positive aspects of your life",
                "steps": [
                    "List 3 things you're grateful for today",
                    "Why are you grateful for each item?",
                    "How did these things make you feel?",
                    "What small thing today brought you joy?",
                    "Who in your life are you thankful for and why?"
                ]
            },
            {
                "name": "Problem Solving",
                "description": "Break down challenges into manageable steps",
                "steps": [
                    "What specific problem are you facing?",
                    "What are all possible solutions (brainstorm without judging)?",
                    "What are the pros and cons of each solution?",
                    "Which solution seems most realistic and helpful?",
                    "What's the first small step you can take?",
                    "When will you take this step?",
                    "How will you know if it's working?"
                ]
            },
            {
                "name": "Mindfulness Check-in",
                "description": "Ground yourself in the present moment",
                "steps": [
                    "Name 5 things you can see around you",
                    "Name 4 things you can touch",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste",
                    "Take 3 deep breaths",
                    "How do you feel right now?"
                ]
            }
        ]
    
    def get_breathing_exercise(self, exercise_name: str = None) -> Dict:
        """Get a specific breathing exercise or random one"""
        if exercise_name:
            for exercise in self.breathing_exercises:
                if exercise["name"].lower() == exercise_name.lower():
                    return exercise
        return random.choice(self.breathing_exercises)
    
    def get_daily_affirmation(self) -> str:
        """Get a random affirmation"""
        return random.choice(self.affirmations)
    
    def get_multiple_affirmations(self, count: int = 3) -> List[str]:
        """Get multiple unique affirmations"""
        return random.sample(self.affirmations, min(count, len(self.affirmations)))
    
    def get_cbt_exercise(self, exercise_name: str = None) -> Dict:
        """Get a specific CBT exercise or random one"""
        if exercise_name:
            for exercise in self.cbt_exercises:
                if exercise["name"].lower() == exercise_name.lower():
                    return exercise
        return random.choice(self.cbt_exercises)
    
    def get_all_exercise_names(self) -> Dict[str, List[str]]:
        """Get names of all available exercises"""
        return {
            "breathing": [ex["name"] for ex in self.breathing_exercises],
            "cbt": [ex["name"] for ex in self.cbt_exercises]
        }
    
    def create_personalized_plan(self, mood_level: int, dominant_emotion: str) -> Dict:
        """Create a personalized self-help plan based on mood and emotion"""
        plan = {
            "recommended_activities": [],
            "affirmations": [],
            "duration_minutes": 0
        }
        
        # Low mood (1-4): Focus on basic grounding and breathing
        if mood_level <= 4:
            plan["recommended_activities"].append(self.get_breathing_exercise("4-7-8 Breathing"))
            plan["recommended_activities"].append(self.get_cbt_exercise("Mindfulness Check-in"))
            plan["affirmations"] = self.get_multiple_affirmations(2)
            plan["duration_minutes"] = 10
        
        # Medium mood (5-7): Include problem solving
        elif mood_level <= 7:
            plan["recommended_activities"].append(self.get_breathing_exercise("Box Breathing"))
            if dominant_emotion in ["sadness", "fear", "pessimism"]:
                plan["recommended_activities"].append(self.get_cbt_exercise("Gratitude Practice"))
            else:
                plan["recommended_activities"].append(self.get_cbt_exercise("Problem Solving"))
            plan["affirmations"] = self.get_multiple_affirmations(3)
            plan["duration_minutes"] = 15
        
        # High mood (8-10): Maintenance and gratitude
        else:
            plan["recommended_activities"].append(self.get_cbt_exercise("Gratitude Practice"))
            plan["affirmations"] = self.get_multiple_affirmations(1)
            plan["duration_minutes"] = 5
        
        return plan

# Global self-help toolkit instance
self_help_toolkit = SelfHelpToolkit()
