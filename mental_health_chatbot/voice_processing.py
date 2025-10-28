import whisper
from gtts import gTTS
import tempfile
import os
from pydub import AudioSegment
import io
import base64
from typing import Optional

class VoiceProcessor:
    def __init__(self):
        self.whisper_model = None
        self.load_whisper_model()
    
    def load_whisper_model(self):
        """Load Whisper model for speech-to-text"""
        try:
            # Load smaller model for faster processing
            self.whisper_model = whisper.load_model("base")
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.whisper_model = None
    
    def speech_to_text(self, audio_file_path: str) -> Optional[str]:
        """Convert speech to text using Whisper"""
        if not self.whisper_model:
            return None
        
        try:
            result = self.whisper_model.transcribe(audio_file_path)
            return result["text"].strip()
        except Exception as e:
            print(f"Error in speech-to-text: {e}")
            return None
    
    def text_to_speech(self, text: str, language: str = "en") -> Optional[str]:
        """Convert text to speech using gTTS and return base64 encoded audio"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                
                # Read the file and encode as base64
                with open(tmp_file.name, "rb") as audio_file:
                    audio_data = audio_file.read()
                    audio_base64 = base64.b64encode(audio_data).decode()
                
                # Clean up temporary file
                os.unlink(tmp_file.name)
                
                return audio_base64
                
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return None
    
    def process_audio_upload(self, audio_data: bytes, file_format: str = "wav") -> Optional[str]:
        """Process uploaded audio data and convert to text"""
        try:
            # Save uploaded audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_format}") as tmp_file:
                tmp_file.write(audio_data)
                tmp_file.flush()
                
                # Convert to text
                transcribed_text = self.speech_to_text(tmp_file.name)
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return transcribed_text
                
        except Exception as e:
            print(f"Error processing audio upload: {e}")
            return None

# Global voice processor instance
voice_processor = VoiceProcessor()
