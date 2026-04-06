"""
Text-to-Speech Service Module

This module handles converting German text to natural-sounding speech.
Uses pyttsx3 (offline TTS) for fast, reliable speech synthesis
without external API dependencies.

Features:
- Offline speech synthesis (no API calls needed)
- Customizable speech rate and volume
- Automatic audio directory management
- Unique file naming to prevent conflicts
- Streaming audio URL generation
"""

import logging
import os
import uuid
from typing import Optional

import pyttsx3

# Setup logging
logger = logging.getLogger(__name__)

# Audio configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "..", "static", "audio")
SPEECH_RATE = 165  # Words per minute (moderate speed for learners)
SPEECH_VOLUME = 1.0  # 0.0 to 1.0

# Global TTS engine instance (created on first use)
_engine = None

logger.info(f"TTS audio directory: {AUDIO_DIR}")

def get_engine():
    """
    Get or initialize the pyttsx3 TTS engine (singleton pattern).
    
    Lazy-loads the TTS engine on first call. Subsequent calls return
    the cached engine instance. Configures speech rate and volume settings.
    
    Returns:
        pyttsx3.TTS.Engine: Initialized text-to-speech engine
    
    Configuration:
        - Speech rate: 165 WPM (moderate for language learners)
        - Volume: 1.0 (maximum)
        - Language: System default (typically German on German systems)
    
    Example:
        >>> engine = get_engine()
        >>> engine.say("Guten Tag")
    """
    global _engine
    if _engine is None:
        logger.info("Initializing pyttsx3 TTS engine...")
        _engine = pyttsx3.init()
        _engine.setProperty("rate", SPEECH_RATE)
        _engine.setProperty("volume", SPEECH_VOLUME)
        logger.info(f"TTS engine initialized: rate={SPEECH_RATE}, volume={SPEECH_VOLUME}")

    return _engine


def synthesize_speech(text: str) -> str:
    """
    Convert German text to speech and save as WAV file.
    
    Synthesizes natural-sounding German speech from input text and saves
    to a unique audio file. Uses pyttsx3 for offline synthesis.
    
    Audio Specifications:
    - Format: WAV (PCM)
    - Sample rate: 16kHz (system default)
    - Channels: Mono
    - Bit depth: 16-bit
    - Naming: reply_{uuid}.wav (ensures uniqueness)
    
    Args:
        text (str): German text to synthesize (non-empty string required)
    
    Returns:
        str: Relative URL path to the generated audio file
              Example: "/static/audio/reply_abc123def456.wav"
    
    Raises:
        ValueError: If text is empty or None
        OSError: If audio directory cannot be created or file cannot be written
        RuntimeError: If TTS engine fails to generate audio
    
    Example:
        >>> audio_url = synthesize_speech("Das ist toll!")
        >>> print(audio_url)
        '/static/audio/reply_abc123def456.wav'
    
    Notes:
        - Audio files are stored in AUDIO_DIR
        - Each call generates a unique filename using UUID4
        - Audio is generated synchronously (blocking call)
    """
    if not text:
        raise ValueError("Text is required for speech synthesis.")

    os.makedirs(AUDIO_DIR, exist_ok=True)
    filename = f"reply_{uuid.uuid4().hex}.wav"
    file_path = os.path.join(AUDIO_DIR, filename)

    try:
        logger.info(f"Synthesizing speech for text: {text[:50]}...")
        engine = get_engine()
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        logger.info(f"Speech synthesis complete: {filename}")
    except Exception as e:
        logger.error(f"Speech synthesis failed: {e}")
        raise RuntimeError(f"Failed to synthesize speech: {e}")

    return f"/static/audio/{filename}"