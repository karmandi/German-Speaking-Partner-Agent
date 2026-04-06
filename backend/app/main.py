"""
German Speaking Partner Agent - FastAPI Backend

A production-ready REST API for AI-powered German language conversation learning.

Features:
- Real-time speech transcription (OpenAI Whisper)
- Natural language generation (GPT-4 via Ollama)
- Text-to-speech synthesis (pyttsx3)
- CORS support for cross-origin requests
- Error handling and validation
- Automatic file cleanup

API Endpoints:
- GET /health - Health check endpoint
- POST /api/speak - Main learning endpoint (multipart/form-data)

Author: German Speaker Agent Project
Version: 1.0.0
"""

import logging
import os
import uuid
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.schemas import TutorResult
from app.services.transcription import transcribe_audio
from app.services.tutor import generate_tutor_reply
from app.services.tts import synthesize_speech

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI application setup
app = FastAPI(
    title="German Speaking Partner Agent",
    description="AI-powered German language learning platform with voice interaction",
    version="1.0.0"
)

# Add CORS middleware first, before all other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    """
    Health check endpoint for monitoring and load balancing.
    
    Returns:
        dict: Status information indicating API availability
        
    Example:
        >>> response = requests.get("http://localhost:8000/health")
        >>> response.json()
        {'status': 'ok'}
    """
    logger.info("Health check requested")
    return {"status": "ok"}


@app.post("/api/speak", response_model=TutorResult)
async def speak(audio: UploadFile = File(...)):
    """
    Main learning endpoint: Accept audio, transcribe, and receive tutoring feedback.
    
    This endpoint orchestrates the complete learning pipeline:
    1. Receives audio file from client
    2. Transcribes speech to text using Whisper
    3. Generates AI tutor response with corrections
    4. Synthesizes audio for the response
    5. Returns complete learning feedback
    
    Request:
        - Content-Type: multipart/form-data
        - Field: audio (file) - WAV, WebM, or MP4 format
    
    Response (TutorResult):
        - user_transcript (str): Recognized German speech
        - assistant_reply_german (str): Natural German response
        - corrected_sentence (str): Corrected version if needed
        - explanation_english (str): Grammar/correction explanation
        - next_question_german (str): Follow-up question
        - level_used (str): Language level (A1, A2, B1)
        - audio_url (str): URL to listen to the response
    
    Raises:
        HTTPException 400: Missing or empty audio file
        HTTPException 500: Processing error (transcription, text-to-speech, etc.)
    
    Performance:
        - Average response time: 2-5 seconds
        - Bottleneck: OpenAI API latency for transcription
    
    Example:
        ```javascript
        const formData = new FormData();
        formData.append('audio', audioBlob, 'speech.wav');
        
        const response = await fetch('/api/speak', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        console.log(result.assistant_reply_german);
        ```
    """
    if not audio.filename:
        logger.warning("Audio request received without filename")
        raise HTTPException(status_code=400, detail="Missing audio filename")

    suffix = os.path.splitext(audio.filename)[1] or ".webm"
    temp_name = f"{uuid.uuid4().hex}{suffix}"
    temp_path = os.path.join(UPLOAD_DIR, temp_name)

    content = await audio.read()
    if not content:
        logger.warning("Audio request received with empty file")
        raise HTTPException(status_code=400, detail="Empty audio file")

    # Save uploaded file temporarily
    with open(temp_path, "wb") as f:
        f.write(content)
    
    logger.info(f"Audio file received: {temp_name}, size: {len(content)} bytes")

    try:
        # Step 1: Transcribe audio
        logger.info("Starting transcription...")
        user_transcript = transcribe_audio(temp_path)
        logger.info(f"Transcription complete: '{user_transcript}'")
        
        # Step 2: Generate tutor reply
        logger.info("Generating tutor response...")
        tutor_data = generate_tutor_reply(user_transcript)
        logger.info("Tutor response generated")
        
        # Step 3: Synthesize response audio
        logger.info("Synthesizing speech...")
        audio_url = synthesize_speech(tutor_data["assistant_reply_german"])
        logger.info(f"Speech synthesis complete")

        response = TutorResult(
            user_transcript=user_transcript,
            assistant_reply_german=tutor_data["assistant_reply_german"],
            corrected_sentence=tutor_data["corrected_sentence"],
            explanation_english=tutor_data["explanation_english"],
            next_question_german=tutor_data["next_question_german"],
            level_used=tutor_data["level_used"],
            audio_url=audio_url,
        )
        logger.info("Request completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing audio: {str(e)}"
        )
    finally:
        # Cleanup: Remove temporary audio file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                logger.info(f"Cleaned up temporary file: {temp_name}")
            except OSError as e:
                logger.warning(f"Failed to clean up {temp_name}: {e}")