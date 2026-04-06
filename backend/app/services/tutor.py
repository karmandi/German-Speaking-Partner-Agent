"""
German Tutor Service Module

This module provides AI-powered tutoring functionality for German language learning.
It handles natural language responses, corrections, and explanations through an
integration with a local LLM model (Ollama/Mistral).

The tutor is designed to:
- Respond naturally in German at the user's language level
- Provide targeted corrections (one mistake per turn)
- Explain corrections in English for clarity
- Ask follow-up questions to continue conversation
- Maintain a friendly, encouraging tone
"""

import json
import logging
import re
from typing import Dict, Optional

import requests
from app.prompts import GERMAN_SPEAKING_PARTNER_PROMPT

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"
REQUEST_TIMEOUT = 60  # seconds

# Setup logging
logger = logging.getLogger(__name__)


def generate_tutor_reply(user_transcript: str) -> dict:
    """
    Generate a natural German tutor response with corrections and explanations.
    
    This function processes user input through a local LLM to generate contextual,
    pedagogically sound responses. The response includes:
    - A natural German reply at the appropriate language level
    - One targeted correction if needed
    - English explanation of the correction
    - A follow-up question to continue the conversation
    
    Args:
        user_transcript (str): The user's spoken input (transcribed German text)
    
    Returns:
        dict: A dictionary containing:
            - assistant_reply_german (str): Natural German response
            - corrected_sentence (str): Corrected version if applicable
            - explanation_english (str): Brief English explanation
            - next_question_german (str): Follow-up question in German
            - level_used (str): Language level (A1, A2, B1)
    
    Raises:
        ValueError: If the model response is empty or invalid
        RequestException: If the Ollama service is unreachable
    
    Example:
        >>> result = generate_tutor_reply("Ich lerne Deutsch jeden Tag.")
        >>> print(result['assistant_reply_german'])
        'Das ist toll! Deutsch jeden Tag zu lernen ist sehr wichtig.'
    """
    prompt = f"{GERMAN_SPEAKING_PARTNER_PROMPT}\nUser said: {user_transcript}"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()

        body = response.json()
        text = body.get("response", "") if isinstance(body, dict) else ""
        if not text:
            raise ValueError("Empty model response")

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            match = re.search(r"(\{.*\})", text, re.S)
            if match:
                return json.loads(match.group(1))
            raise
    except Exception:
        return {
            "assistant_reply_german": "Kannst du das bitte wiederholen?",
            "corrected_sentence": user_transcript,
            "explanation_english": "The assistant could not parse the reply. Please try again.",
            "next_question_german": "Kannst du einen einfachen Satz sagen?",
            "level_used": "A1",
        }