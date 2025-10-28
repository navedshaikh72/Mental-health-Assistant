from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, List
import logging

class EmotionDetector:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"
        self.tokenizer = None
        self.model = None
        self.emotion_labels = ["anger", "anticipation", "disgust", "fear", "joy", "love", "optimism", "pessimism", "sadness", "surprise", "trust"]
        self.load_model()
    
    def load_model(self):
        """Load the emotion detection model"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            print("Emotion detection model loaded successfully")
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            print("Using fallback emotion detection...")
            self.model = None
    
    def detect_emotions(self, text: str) -> Dict[str, float]:
        """Detect emotions in text and return probabilities"""
        if not self.model or not text.strip():
            return self._fallback_emotion_detection(text)
        
        try:
            # Tokenize and predict
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.sigmoid(outputs.logits).squeeze().numpy()
            
            # Create emotion dictionary
            emotions = {}
            for i, label in enumerate(self.emotion_labels):
                emotions[label] = float(probabilities[i])
            
            return emotions
            
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return self._fallback_emotion_detection(text)
    
    def _fallback_emotion_detection(self, text: str) -> Dict[str, float]:
        """Simple keyword-based emotion detection as fallback"""
        text_lower = text.lower()
        emotions = {label: 0.0 for label in self.emotion_labels}
        
        # Simple keyword matching
        emotion_keywords = {
            "joy": ["happy", "joyful", "excited", "great", "wonderful", "amazing", "fantastic"],
            "sadness": ["sad", "depressed", "down", "unhappy", "miserable", "gloomy"],
            "anger": ["angry", "mad", "furious", "irritated", "annoyed", "rage"],
            "fear": ["scared", "afraid", "anxious", "worried", "nervous", "terrified"],
            "surprise": ["surprised", "shocked", "amazed", "astonished"],
            "disgust": ["disgusted", "revolted", "repulsed", "sick"],
            "trust": ["trust", "confident", "secure", "safe", "reliable"],
            "anticipation": ["excited", "looking forward", "anticipating", "eager"],
            "love": ["love", "adore", "cherish", "affection", "care"],
            "optimism": ["optimistic", "hopeful", "positive", "bright"],
            "pessimism": ["pessimistic", "hopeless", "negative", "dark"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotions[emotion] += 0.3
        
        # Normalize values
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    def get_dominant_emotion(self, emotions: Dict[str, float]) -> str:
        """Get the emotion with highest probability"""
        if not emotions:
            return "neutral"
        return max(emotions.items(), key=lambda x: x[1])[0]

# Global emotion detector instance
emotion_detector = EmotionDetector()
