import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
import io
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from database import MoodEntry, ChatMessage
import json

class DataVisualizer:
    def __init__(self):
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_mood_trend_chart(self, db: Session, days: int = 30) -> str:
        """Create mood trend chart for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query mood entries
        mood_entries = db.query(MoodEntry).filter(
            MoodEntry.date >= start_date,
            MoodEntry.date <= end_date
        ).order_by(MoodEntry.date).all()
        
        if not mood_entries:
            return self._create_no_data_chart("No mood data available for the selected period")
        
        # Prepare data
        dates = [entry.date.date() for entry in mood_entries]
        ratings = [entry.mood_rating for entry in mood_entries]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot mood trend
        ax.plot(dates, ratings, marker='o', linewidth=2, markersize=6)
        ax.fill_between(dates, ratings, alpha=0.3)
        
        # Customize chart
        ax.set_title(f'Mood Trend - Last {days} Days', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Mood Rating (1-10)', fontsize=12)
        ax.set_ylim(1, 10)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._save_plot_as_base64(fig)
    
    def create_emotion_distribution_chart(self, db: Session, days: int = 30) -> str:
        """Create emotion distribution pie chart"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query entries with emotions
        entries = db.query(MoodEntry).filter(
            MoodEntry.date >= start_date,
            MoodEntry.date <= end_date,
            MoodEntry.detected_emotions.isnot(None)
        ).all()
        
        if not entries:
            return self._create_no_data_chart("No emotion data available")
        
        # Aggregate emotions
        emotion_totals = {}
        for entry in entries:
            if entry.detected_emotions:
                emotions = json.loads(entry.detected_emotions) if isinstance(entry.detected_emotions, str) else entry.detected_emotions
                for emotion, score in emotions.items():
                    emotion_totals[emotion] = emotion_totals.get(emotion, 0) + score
        
        # Get top 8 emotions
        top_emotions = dict(sorted(emotion_totals.items(), key=lambda x: x[1], reverse=True)[:8])
        
        if not top_emotions:
            return self._create_no_data_chart("No emotion data to display")
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_emotions)))
        wedges, texts, autotexts = ax.pie(
            top_emotions.values(), 
            labels=top_emotions.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        ax.set_title(f'Emotion Distribution - Last {days} Days', fontsize=16, fontweight='bold')
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        return self._save_plot_as_base64(fig)
    
    def create_weekly_mood_heatmap(self, db: Session, weeks: int = 12) -> str:
        """Create weekly mood heatmap"""
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        # Query mood entries
        mood_entries = db.query(MoodEntry).filter(
            MoodEntry.date >= start_date,
            MoodEntry.date <= end_date
        ).all()
        
        if not mood_entries:
            return self._create_no_data_chart("No mood data available for heatmap")
        
        # Create DataFrame
        df = pd.DataFrame([
            {
                'date': entry.date.date(),
                'weekday': entry.date.strftime('%A'),
                'week': entry.date.isocalendar()[1],
                'mood': entry.mood_rating
            }
            for entry in mood_entries
        ])
        
        # Pivot for heatmap
        heatmap_data = df.pivot_table(
            values='mood', 
            index='weekday', 
            columns='week', 
            aggfunc='mean'
        )
        
        # Reorder weekdays
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(weekday_order)
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 6))
        
        sns.heatmap(
            heatmap_data, 
            annot=True, 
            cmap='RdYlGn', 
            center=5.5,
            vmin=1, 
            vmax=10,
            ax=ax,
            cbar_kws={'label': 'Average Mood Rating'}
        )
        
        ax.set_title(f'Weekly Mood Heatmap - Last {weeks} Weeks', fontsize=16, fontweight='bold')
        ax.set_xlabel('Week Number', fontsize=12)
        ax.set_ylabel('Day of Week', fontsize=12)
        
        plt.tight_layout()
        return self._save_plot_as_base64(fig)
    
    def create_mood_emotion_correlation(self, db: Session, days: int = 30) -> str:
        """Create correlation chart between mood ratings and emotions"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        entries = db.query(MoodEntry).filter(
            MoodEntry.date >= start_date,
            MoodEntry.date <= end_date,
            MoodEntry.detected_emotions.isnot(None)
        ).all()
        
        if not entries:
            return self._create_no_data_chart("No data available for correlation analysis")
        
        # Prepare data
        data_for_correlation = []
        for entry in entries:
            emotions = json.loads(entry.detected_emotions) if isinstance(entry.detected_emotions, str) else entry.detected_emotions
            row = {'mood_rating': entry.mood_rating}
            row.update(emotions)
            data_for_correlation.append(row)
        
        df = pd.DataFrame(data_for_correlation)
        
        # Select top emotions by variance
        emotion_cols = [col for col in df.columns if col != 'mood_rating']
        emotion_variances = df[emotion_cols].var().sort_values(ascending=False)
        top_emotions = emotion_variances.head(6).index.tolist()
        
        # Create correlation matrix
        correlation_data = df[['mood_rating'] + top_emotions].corr()
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(
            correlation_data,
            annot=True,
            cmap='coolwarm',
            center=0,
            ax=ax,
            square=True
        )
        
        ax.set_title('Mood-Emotion Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return self._save_plot_as_base64(fig)
    
    def _create_no_data_chart(self, message: str) -> str:
        """Create a chart showing no data message"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, message, fontsize=16, ha='center', va='center', transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return self._save_plot_as_base64(fig)
    
    def _save_plot_as_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)  # Close figure to free memory
        return image_base64
    
    def generate_comprehensive_report(self, db: Session, days: int = 30) -> Dict[str, str]:
        """Generate comprehensive visual report"""
        return {
            "mood_trend": self.create_mood_trend_chart(db, days),
            "emotion_distribution": self.create_emotion_distribution_chart(db, days),
            "weekly_heatmap": self.create_weekly_mood_heatmap(db, min(days//7, 12)),
            "mood_emotion_correlation": self.create_mood_emotion_correlation(db, days)
        }

# Global visualizer instance
data_visualizer = DataVisualizer()
