from pydantic import BaseModel
from typing import Literal

class TutorResult(BaseModel):
    user_transcript: str
    assistant_reply_german: str
    corrected_sentence: str
    explanation_english: str
    next_question_german: str
    level_used: Literal["A1", "A2", "B1"]
    audio_url: str