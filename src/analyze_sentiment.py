import pandas as pd
from textblob import TextBlob
from src.constants import MIN_CHAR_LENGTH
from pathlib import Path

def get_sentiment(text):
    if not text or not isinstance(text, str) or MIN_CHAR_LENGTH > len(text) :
        return 0.0, 0.0
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity
