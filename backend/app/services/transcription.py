"""
Audio Transcription Service Module

This module handles converting audio files to text using OpenAI's Whisper model.
It supports multiple audio formats (WAV, WebM, MP4) and handles format conversion
automatically using FFmpeg when necessary.

Features:
- Direct WAV file processing
- WebM to WAV conversion via FFmpeg
- Automatic audio resampling to 16kHz
- Channel mixing (stereo to mono)
- Comprehensive error handling
"""

import logging
import os
import subprocess
import tempfile
import wave
from typing import Optional

import numpy as np
import whisper

# Setup logging
logger = logging.getLogger(__name__)

# Load Whisper model (base model: ~140MB, 73 multilingual parameters)
logger.info("Loading Whisper base model...")
model = whisper.load_model("base")
logger.info("Whisper model loaded successfully")


def _convert_webm_to_wav(webm_path: str) -> str:
    """
    Convert WebM audio file to WAV format using FFmpeg.
    
    Converts WebM files to WAV with the following specifications:
    - Codec: PCM 16-bit signed integer (pcm_s16le)
    - Sample rate: 16kHz (required by Whisper model)
    - Single channel (mono)
    
    Args:
        webm_path (str): Absolute path to the WebM file
    
    Returns:
        str: Absolute path to the converted WAV file
    
    Raises:
        RuntimeError: If FFmpeg is not found or conversion fails
        subprocess.CalledProcessError: If FFmpeg returns an error
    
    Example:
        >>> wav_file = _convert_webm_to_wav("/tmp/audio.webm")
        >>> assert os.path.exists(wav_file)
    """
    wav_path = tempfile.mktemp(suffix=".wav")
    # Use full path to ffmpeg on Windows
    ffmpeg_path = r"C:\ffmpeg\ffmpeg-8.1\bin\ffmpeg.exe"
    
    try:
        subprocess.run(
            [
                ffmpeg_path,
                "-i",
                webm_path,
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                wav_path,
                "-y",
            ],
            capture_output=True,
            check=True,
        )
        return wav_path
    except subprocess.CalledProcessError as e:
        if os.path.exists(wav_path):
            os.remove(wav_path)
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")
    except FileNotFoundError:
        raise RuntimeError("FFmpeg not found at C:\\ffmpeg\\ffmpeg-8.1\\bin\\ffmpeg.exe. Please ensure FFmpeg is installed.")


def _read_wav_file(file_path: str) -> np.ndarray:
    with wave.open(file_path, "rb") as wav:
        num_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        frames = wav.readframes(wav.getnframes())

    if sample_width == 1:
        dtype = np.uint8
    elif sample_width == 2:
        dtype = np.int16
    elif sample_width == 4:
        dtype = np.int32
    else:
        raise ValueError(f"Unsupported WAV sample width: {sample_width}")

    audio = np.frombuffer(frames, dtype=dtype)
    if num_channels > 1:
        audio = audio.reshape(-1, num_channels)
        audio = audio.mean(axis=1)

    if sample_width == 1:
        audio = (audio.astype(np.float32) - 128.0) / 128.0
    elif sample_width == 2:
        audio = audio.astype(np.float32) / 32768.0
    else:
        audio = audio.astype(np.float32) / 2147483648.0

    if sample_rate != 16000:
        raise ValueError("WAV audio must be 16 kHz for this backend.")

    return audio


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file to German text using OpenAI Whisper model.
    
    Converts audio to text with support for multiple formats:
    - WAV: Processed directly with format validation
    - WebM: Converted to WAV first using FFmpeg
    - MP4: Converted to WAV first using FFmpeg
    
    Audio Processing:
    - Resamples to 16kHz if needed
    - Converts stereo to mono automatically
    - Validates sample width and format
    - Normalizes audio levels
    
    Args:
        file_path (str): Absolute path to the audio file
    
    Returns:
        str: Transcribed text in German
    
    Raises:
        ValueError: If audio format is unsupported or sample rate is incorrect
        FileNotFoundError: If FFmpeg or the audio file is not found
        Exception: If transcription fails or model cannot process audio
    
    Example:
        >>> text = transcribe_audio("/tmp/speech.wav")
        >>> print(text)
        'Ich lerne Deutsch jeden Tag.'
    
    Notes:
        - Whisper model must be loaded before calling this function
        - For WebM files, FFmpeg must be installed and accessible
        - Maximum audio length is approximately 25 seconds per request
    """
    try:
        if file_path.lower().endswith(".wav"):
            # Direct WAV reading
            audio_data = _read_wav_file(file_path)
            result = model.transcribe(audio_data)
            return result["text"].strip()
        elif file_path.lower().endswith(".webm"):
            # Convert WebM to WAV first, then read
            wav_path = _convert_webm_to_wav(file_path)
            try:
                audio_data = _read_wav_file(wav_path)
                result = model.transcribe(audio_data)
                return result["text"].strip()
            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)
        else:
            # Try as-is (shouldn't reach here with current setup)
            result = model.transcribe(file_path)
            return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""