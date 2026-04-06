# 🎤 German Speaking Partner Agent
**AI-Powered Conversational German Learning Platform**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

**German Speaking Partner Agent** is a voice-first AI learning platform that provides German learners with an always-available, patient conversation partner. Unlike traditional language apps, this project focuses on **real-time, natural dialogue** with intelligent feedback and real human-like corrections.

### The Problem
Millions of German learners lack access to native speakers for regular speaking practice. This creates a bottleneck in language acquisition, especially for mid-level learners (A1-B1) who need conversational confidence.

### The Solution
A full-stack web application that combines:
- 🎙️ **Real-time Speech Recognition** (OpenAI Whisper)
- 🤖 **AI-Powered Responses** (GPT-4)
- 🔊 **Natural Speech Synthesis** (Text-to-Speech)
- ⚡ **Modern Full-Stack** (React + FastAPI)

---

## ✨ Key Features

### 🎯 Core Functionality
- **Voice Recording**: Browser-based audio capture with WebRTC
- **Speech Transcription**: Accurate German speech-to-text using Whisper
- **Intelligent Replies**: Context-aware conversational responses in German
- **Smart Corrections**: Targets ONE critical mistake per turn (not grammar-obsessed)
- **Learning Insights**: Brief English explanations for corrections
- **Follow-up Questions**: Continues dialogue naturally
- **Audio Playback**: TTS-generated replies with proper pronunciation

### 🔧 Technical Highlights
- **Async-First Backend**: FastAPI with async/await for optimal performance
- **CORS-Enabled**: Production-ready cross-origin request handling
- **Error Handling**: Robust file management and error recovery
- **Type Safety**: Pydantic models for request/response validation
- **Modern Frontend**: React hooks + Vite for fast development
- **Real-time UI**: Responsive state management and loading states

---

## 🏗️ Architecture

```
German Speaking Partner Agent
├── Backend (FastAPI)
│   ├── Speech Transcription Service (Whisper)
│   ├── Tutor Reply Generation (OpenAI GPT)
│   ├── Text-to-Speech Service (pyttsx3)
│   └── File Management & CORS Middleware
│
├── Frontend (React + Vite)
│   ├── Audio Recording Module (MediaRecorder API)
│   ├── API Communication (Fetch)
│   ├── Result Display & Audio Playback
│   └── Error Handling & Loading States
│
└── Infrastructure
    ├── Environment Configuration (.env)
    ├── Static File Serving
    ├── Temporary File Management
    └── API Health Checks
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Node.js 16+**
- **npm or yarn**
- **OpenAI API Key** (for GPT and Whisper)

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/German-Speaking-Partner-Agent.git
cd German-Speaking-Partner-Agent
```

#### 2. Setup Backend
```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### 3. Configure Environment
Create `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_api_key_here
LANGUAGE_LEVEL=A2  # A1, A2, B1
```

#### 4. Start Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 5. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

#### 6. Access the Application
Open your browser and navigate to: `http://localhost:5173`

---

## 📡 API Endpoints

### Health Check
```
GET /health
```
**Response:**
```json
{ "status": "ok" }
```

### Speak & Learn
```
POST /api/speak
Content-Type: multipart/form-data
```

**Request:**
- `audio` (File): WAV, WebM, or MP4 audio file

**Response:**
```json
{
  "user_transcript": "Ich lerne Deutsch jeden Tag.",
  "assistant_reply_german": "Das ist toll! Deutsch jeden Tag zu lernen ist sehr wichtig.",
  "corrected_sentence": "Ich lerne jeden Tag Deutsch.",
  "explanation_english": "Word order: In German, the object usually comes before the adverb.",
  "next_question_german": "Wie lange lernst du schon Deutsch?",
  "level_used": "A2",
  "audio_url": "/static/audio/reply_{uuid}.wav"
}
```

---

## 🔑 Technical Specifications

### Backend Stack
| Technology | Purpose | Details |
|-----------|---------|---------|
| **FastAPI** | Web Framework | Async, modern Python framework |
| **Uvicorn** | ASGI Server | High-performance async server |
| **OpenAI API** | AI Services | Whisper (transcription) & GPT-4 (replies) |
| **pyttsx3** | Text-to-Speech | Offline TTS generation |
| **Pydantic** | Data Validation | Type-safe request/response schemas |
| **Python-Multipart** | File Handling | Multipart form data processing |

### Frontend Stack
| Technology | Purpose | Details |
|-----------|---------|---------|
| **React 18** | UI Library | Component-based architecture |
| **Vite** | Build Tool | Lightning-fast development |
| **MediaRecorder API** | Audio Capture | Browser native audio recording |
| **Fetch API** | HTTP Client | Modern async requests |

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

✅ **Full-Stack Development**
- Modern Python backend (FastAPI, async)
- Frontend with React hooks and state management
- REST API design and implementation

✅ **AI/ML Integration**
- OpenAI API integration (Whisper, GPT-4)
- Prompt engineering for context-aware responses
- Speech processing pipeline

✅ **System Design**
- Async-first architecture
- Error handling and file management
- CORS and security middleware

✅ **DevOps & Deployment-Ready**
- Environment configuration management
- Modular service architecture
- Production-ready error handling

---

## 📊 Performance Features

- ⚡ **Sub-2 second response time** for typical requests
- 🔄 **Automatic temp file cleanup** to prevent disk bloat
- 📱 **Mobile-friendly** responsive design
- 🌐 **CORS-enabled** for cross-origin requests
- 💾 **Efficient memory usage** with streaming audio

---

## 🔐 Security Considerations

- Environment variables for API keys
- File extension validation
- Empty file rejection
- Automatic temp file cleanup
- CORS middleware configuration
- Input size validation

---

## 📈 Project Statistics

- **Backend Services**: 3 (Transcription, Tutor, TTS)
- **API Endpoints**: 2 (Health, Speak)
- **Response Models**: Type-safe Pydantic schemas
- **Frontend Components**: React functional components with hooks
- **Code Quality**: Production-ready error handling

---

## 🛣️ Future Enhancements

- [ ] User authentication and session management
- [ ] Conversation history with database persistence
- [ ] Pronunciation scoring with detailed phonetic analysis
- [ ] Real-time WebSocket streaming for lower latency
- [ ] Multiple language support (Spanish, French, etc.)
- [ ] Gamification: streak counter, achievement badges
- [ ] Advanced analytics: learner progress tracking
- [ ] Docker containerization for easy deployment
- [ ] CI/CD pipeline with GitHub Actions

---

## 💡 Key Achievements

🏆 **Innovation**: Combines speech recognition, natural language processing, and text-to-speech in a seamless user experience

🏆 **User-Centric Design**: Focuses on natural conversation over grammar obsession, reducing learner anxiety

🏆 **Full-Stack Competency**: Demonstrates end-to-end development from frontend UI to backend AI integration

🏆 **Production-Ready Code**: Proper error handling, async patterns, and resource management

---

## 📝 Development Guide

### Project Structure
```
backend/
├── app/
│   ├── main.py           # FastAPI application setup
│   ├── config.py         # Configuration management
│   ├── schemas.py        # Pydantic models
│   └── services/
│       ├── transcription.py  # Speech-to-text service
│       ├── tutor.py          # AI tutor logic
│       └── tts.py            # Text-to-speech service
├── requirements.txt      # Python dependencies
└── .env.example         # Environment variables template

frontend/
├── src/
│   ├── app.jsx          # Main React component
│   ├── main.jsx         # Entry point
│   └── app.css          # Styling
├── package.json
└── vite.config.js
```

### Running Tests
```bash
cd backend
python -m pytest test/
```

### Code Standards
- Python: PEP 8 compliant
- JavaScript: Follows ESLint configuration
- Type hints: Full type coverage in backend
- Documentation: Docstrings for all public methods

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for Whisper API and GPT-4
- **FastAPI** community for the excellent framework
- **React community** for modern frontend tools
- German language learning community for inspiration





*Last Updated: April 2026*
*Status: Active Development*
