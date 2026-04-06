# German Speaking Partner Agent — Project Overview

## 1. Project Summary

This project is a voice-first AI German speaking partner for learners who do not have easy access to native speakers for daily speaking practice.

The goal is to create a practical, human-like conversation partner that:
- listens to the learner's speech,
- replies naturally in simple German,
- corrects only the most important mistake,
- explains the correction briefly in English,
- asks one follow-up question to continue the conversation.

The product is designed to feel like a real-life speaking partner, not a strict grammar checker.

---

## 2. Main Problem

Many German learners:
- do not have native speakers around them,
- cannot practice speaking regularly,
- feel afraid of making mistakes,
- want natural conversation instead of textbook exercises.

This project solves that by providing a low-pressure, always-available speaking companion.

---

## 3. Main Goal

Build an MVP that allows the user to:
1. record audio in the browser,
2. send the audio to the backend,
3. transcribe the speech,
4. generate a natural German reply,
5. provide one correction and a short explanation,
6. generate speech audio for the reply,
7. play the reply back in the browser.

---

## 4. MVP Scope

### Included
- audio recording from browser,
- audio upload to FastAPI backend,
- speech transcription,
- German partner response generation,
- one correction per turn,
- short English explanation,
- one follow-up question,
- text-to-speech playback,
- simple React interface.

### Not included in MVP
- login system,
- database memory,
- pronunciation scoring,
- realtime voice streaming,
- user analytics,
- streaks/gamification,
- multi-agent architecture.

---

## 5. Target Users

### Primary users
- A1, A2, and B1 German learners,
- learners living in Germany,
- students and job seekers,
- people who want practical speaking practice for daily life.

### Example use cases
- daily conversation practice,
- job interview practice,
- supermarket / doctor / landlord roleplay,
- confidence building for speaking.

---

## 6. Product Behavior

The assistant should behave like:
- a patient conversation partner,
- natural and friendly,
- simple and clear,
- encouraging but not overly emotional,
- focused on communication first.

### Correction policy
- correct only one important mistake per turn,
- do not interrupt fluency too much,
- prioritize confidence and understanding,
- adapt language level to the learner.

---

## 7. High-Level Architecture

```text
Frontend (React)
    ↓
Audio recording in browser
    ↓
POST /api/speak
    ↓
Backend (FastAPI)
    ├─ save uploaded audio
    ├─ transcribe audio
    ├─ generate tutor reply
    ├─ synthesize speech
    └─ return JSON + audio URL
    ↓
Frontend displays result + plays audio
```

---

## 8. Tech Stack

### Frontend
- React
- Vite
- MediaRecorder API
- HTML audio player

### Backend
- FastAPI
- Uvicorn
- Python

### AI / Speech Layer
Possible options:

#### Cloud-based
- OpenAI transcription
- OpenAI text generation
- OpenAI TTS

#### Local / open-source
- Whisper for transcription
- Ollama for local LLM inference
- pyttsx3 or Coqui TTS for local speech synthesis

---

## 9. Current Recommended Development Path

For easiest testing without API billing:
- transcription: mock response first, then Whisper later,
- reply generation: Ollama with Mistral or Phi,
- TTS: pyttsx3,
- frontend: React,
- backend: FastAPI.

This allows the team to validate the interaction flow before optimizing model quality.

---

## 10. Project Structure

```text
German Agent/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ config.py
│  │  ├─ prompts.py
│  │  ├─ schemas.py
│  │  ├─ services/
│  │  │  ├─ transcription.py
│  │  │  ├─ tutor.py
│  │  │  └─ tts.py
│  │  └─ static/
│  │     ├─ audio/
│  │     └─ uploads/
│  └─ requirements.txt
└─ frontend/
   ├─ index.html
   ├─ package.json
   ├─ vite.config.js
   └─ src/
      ├─ main.jsx
      ├─ App.jsx
      └─ app.css
```

---

## 11. Backend Responsibilities

### `main.py`
- defines FastAPI app,
- handles CORS,
- exposes `/health`,
- exposes `/api/speak`,
- coordinates upload → transcription → reply → TTS.

### `schemas.py`
- defines response models.

### `prompts.py`
- stores the German partner system prompt.

### `services/transcription.py`
- turns audio into text.

### `services/tutor.py`
- generates structured German partner output.

### `services/tts.py`
- turns assistant reply text into playable audio.

---

## 12. Frontend Responsibilities

### `App.jsx`
- starts/stops recording,
- uploads audio blob,
- receives backend response,
- displays transcript, correction, explanation, next question,
- plays generated audio.

### `main.jsx`
- renders React app.

### `app.css`
- basic styling.

### `index.html`
- root HTML for Vite app.

---

## 13. API Design

### Health check
`GET /health`

Response:
```json
{
  "status": "ok"
}
```

### Main endpoint
`POST /api/speak`

Input:
- multipart form data,
- audio file from browser.

Output:
```json
{
  "user_transcript": "Ich lerne Deutsch jeden Tag.",
  "assistant_reply_german": "Das ist sehr gut. Warum lernst du Deutsch?",
  "corrected_sentence": "Ich lerne jeden Tag Deutsch.",
  "explanation_english": "The word order is more natural this way.",
  "next_question_german": "Was machst du, um Deutsch zu üben?",
  "level_used": "A2",
  "audio_url": "/static/audio/reply_xxx.wav"
}
```

---

## 14. Prompt Design

The prompt must force the model to behave as a speaking partner, not a teacher.

### Required behavior
- reply in simple German,
- sound natural and patient,
- correct one important mistake,
- give very short English explanation,
- ask exactly one follow-up question,
- return strict JSON.

This reduces randomness and makes integration easier.

---

## 15. Local Model Strategy

### Local transcription
Whisper can be used for offline transcription, but on Windows it requires FFmpeg to decode formats like `.webm`.

### Local LLM
Ollama can run models like:
- `mistral`
- `phi3`
- `llama3`

### Local TTS
- `pyttsx3` is easier on Windows,
- Coqui TTS can offer better quality but may be heavier.

---

## 16. Development Stages

### Stage 1 — MVP
- mock or local transcription,
- local reply generation,
- local TTS,
- browser-based recording,
- complete request/response cycle.

### Stage 2 — Better quality
- improve prompt,
- better German response quality,
- add level selection,
- add roleplay modes.

### Stage 3 — Memory
- save past mistakes,
- learner profile,
- repeated correction tracking.

### Stage 4 — Realtime voice
- move from upload-based flow to live conversation,
- use streaming or Realtime architecture.

---

## 17. Main Risks

### Technical risks
- Whisper on Windows requires FFmpeg,
- local TTS may be inconsistent,
- browser audio formats can vary,
- local models may return bad JSON.

### Product risks
- too many corrections make the app feel robotic,
- weak voice quality reduces realism,
- overly complex MVP slows delivery.

---

## 18. Recommended Simplifications

To finish and test faster:
- mock transcription first if needed,
- use one local model only,
- use one fixed level (A2),
- avoid databases at first,
- focus on one clean conversation flow.

---

## 19. Success Criteria for MVP

The MVP is successful if:
1. user can open the app,
2. record a sentence,
3. receive a German reply,
4. see one correction,
5. hear the reply audio,
6. continue practicing with the next question.

---

## 20. Future Improvements

- roleplay modes,
- user level selection,
- session history,
- saved mistakes,
- dashboard for progress,
- multilingual explanations,
- realtime speech-to-speech conversation,
- pronunciation feedback,
- mobile version,
- production deployment.

---

## 21. Run Instructions

### Backend
```powershell
cd "C:\Users\HORNY\OneDrive\Bureau\German Agent\backend"
& "C:\Users\HORNY\OneDrive\Bureau\German Agent\.venv\Scripts\Activate.ps1"
uvicorn app.main:app --reload
```

### Frontend
```powershell
cd "C:\Users\HORNY\OneDrive\Bureau\German Agent\frontend"
npm install
npm run dev
```

Frontend URL:
```text
http://localhost:5173/
```

Backend URL:
```text
http://127.0.0.1:8000/
```

---

## 22. Final Positioning Statement

**German Speaking Partner Agent** is a focused voice-based AI product that helps learners practice practical spoken German through natural conversation, light correction, and human-like interaction.

It is not a general assistant.
It is a task-specific language practice agent.
