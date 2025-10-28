# Mental Health AI Assistant

A sophisticated generative AI system that provides mental health support through voice chat, mood tracking, and analytics. Built with Flutter (frontend) and Python FastAPI (backend).

## 🎯 Project Overview

This application demonstrates mastery of generative AI technologies including:
- **Prompt Engineering**: Systematic prompting strategies for mental health conversations
- **Multimodal Integration**: Voice chat with speech-to-text and text-to-speech capabilities
- Real-time emotion detection and mood analysis
- Comprehensive analytics and data visualization

## 🏗️ Project Structure

```
Mental-Health-AI-Assistant/
├── mental_health_chatbot/          # Python Backend (FastAPI)
│   ├── chatbot_api.py             # Main API server
│   ├── database.py                # Database models
│   ├── emotion_detection.py       # AI emotion analysis
│   ├── voice_processing.py        # Speech processing
│   ├── requirements.txt           # Python dependencies
│   └── chatbot_env/              # Virtual environment
│
├── mental_health_chat_ui/          # Flutter Frontend
│   ├── lib/                      # Dart source code
│   ├── android/                  # Android platform
│   ├── ios/                      # iOS platform
│   ├── web/                      # Web platform
│   ├── windows/                  # Windows platform
│   └── pubspec.yaml             # Flutter dependencies
│
├── mental_health.db               # SQLite database
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Flutter SDK** - [Download Flutter](https://docs.flutter.dev/get-started/install)
- **Git** - [Download Git](https://git-scm.com/downloads)

### 1. Clone the Repository

```bash
git clone https://github.com/HiteshSonetaNEU/Mental-health-Assistant
cd Mental-Health-AI-Assistant
```

### 2. Backend Setup (Python)

```bash
# Navigate to backend directory
cd mental_health_chatbot

# Create virtual environment (recommended)
python -m venv chatbot_env

# Activate virtual environment
# On Windows:
chatbot_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python chatbot_api.py
```

The backend will be available at:
- **API**: http://127.0.0.1:8000
- **Documentation**: http://127.0.0.1:8000/docs

### 3. Flutter Setup & Frontend

#### Install Flutter SDK

1. **Download Flutter**:
   - Visit [Flutter Install Guide](https://docs.flutter.dev/get-started/install/windows)
   - Download Flutter SDK for Windows
   - Extract to `C:\flutter` (or your preferred location)

2. **Add Flutter to PATH**:
   ```bash
   # Add to your system PATH environment variable:
   C:\flutter\bin
   ```

3. **Verify Installation**:
   ```bash
   flutter doctor
   ```

4. **Enable Web Support**:
   ```bash
   flutter config --enable-web
   ```

#### Run Frontend

```bash
# Navigate to frontend directory
cd mental_health_chat_ui

# Install dependencies
flutter pub get

# Run on Chrome (Recommended)
flutter run -d chrome

# Alternative: Run on web server
flutter run -d web-server --web-port 3000
```

The frontend will be available at:
- **Chrome App**: Automatically opens
- **Web Server**: http://localhost:3000

## 🎯 Features

### 🗣️ Voice Chat
- Real-time speech-to-text conversion
- AI-powered text-to-speech responses
- Multimodal conversation experience

### 📊 Mood Tracking
- Daily mood journal entries
- Emotion detection and analysis
- Mood rating system (1-10)

### 📈 Analytics Dashboard
- Mood trends visualization
- Weekly activity patterns
- Data export functionality

### 🧘 Self-Help Tools
- Guided breathing exercises
- Cognitive Behavioral Therapy (CBT) techniques
- Daily affirmations

## 🛠️ Development

### Backend API Endpoints

- `POST /chat` - Chat with AI assistant
- `POST /mood-entry` - Save mood journal entries
- `GET /analytics/mood-trends` - Get mood analytics
- `GET /analytics/weekly-patterns` - Get activity patterns
- `GET /self-help-recommendations` - Get self-help suggestions

### Frontend Screens

- **Chat Screen**: Voice/text chat with AI
- **Mood Journal**: Daily mood tracking
- **Analytics**: Data visualization
- **Self-Help**: Wellness activities

### Database Schema

- **MoodEntry**: Mood ratings and journal entries
- **ChatMessage**: Conversation history
- **SelfHelpActivity**: Completed wellness activities

## 🔧 Troubleshooting

### Common Issues

1. **Flutter not found**:
   ```bash
   # Ensure Flutter is in PATH
   echo $env:PATH | Select-String flutter
   ```

2. **Backend dependencies**:
   ```bash
   # Reinstall Python packages
   pip install --force-reinstall -r requirements.txt
   ```

3. **Database issues**:
   ```bash
   # Delete and recreate database
   rm mental_health.db
   python chatbot_api.py  # Will recreate automatically
   ```

4. **Port conflicts**:
   ```bash
   # Kill processes using port 8000
   taskkill /F /IM python.exe
   ```

### Flutter Doctor Issues

```bash
# Check Flutter installation
flutter doctor -v

# Accept Android licenses (if using Android)
flutter doctor --android-licenses

# Update Flutter
flutter upgrade
```

## 📱 Platform Support

- ✅ **Web** (Chrome, Firefox, Safari)
- ✅ **Windows** (Desktop app)
- ✅ **Android** (Mobile app)
- ✅ **iOS** (Mobile app)

## 🔒 Privacy & Security

- All data stored locally in SQLite database
- No external data transmission except to AI model API
- Voice processing handled locally when possible
- User data can be exported/deleted at any time

## 📚 Technical Stack

### Backend
- **Python 3.11+** - Core language
- **FastAPI** - Web framework
- **SQLite** - Database
- **Transformers** - AI models
- **Whisper** - Speech recognition
- **TTS** - Text-to-speech

### Frontend
- **Flutter** - Cross-platform framework
- **Dart** - Programming language
- **HTTP** - API communication
- **Speech-to-Text** - Voice input
- **Flutter TTS** - Voice output

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review [Flutter documentation](https://docs.flutter.dev/)
3. Check [FastAPI documentation](https://fastapi.tiangolo.com/)
4. Open an issue in the repository

---

## 🎓 Assignment Requirements Met

### Core Components
- ✅ **Prompt Engineering**: Systematic mental health conversation prompts
- ✅ **Multimodal Integration**: Voice + text chat capabilities

### Technical Implementation
- ✅ Complete source code with documentation
- ✅ Cross-platform Flutter application
- ✅ RESTful API with comprehensive endpoints
- ✅ Real-time AI emotion detection
- ✅ Data visualization and analytics

### User Experience
- ✅ Intuitive voice chat interface
- ✅ Responsive design across platforms
- ✅ Error handling and recovery
- ✅ Performance optimization

---

**Built with ❤️ for mental health support**
