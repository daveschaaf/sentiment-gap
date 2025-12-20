import pandas as pd
from textblob import TextBlob
from src.constants import MIN_CHAR_LENGTH
from pathlib import Path

def get_sentiment(text):
    if not text or not isinstance(text, str) or MIN_CHAR_LENGTH > len(text) :
        return 0.0, 0.0
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

if __name__ == "__main__":
    processed_data =  Path("data", "processed", "health_and_personal_care.pkl")
    df = pd.read_pickle(processed_data)
    print("Analyzing sentiment and subjectivity...")
    df[['review_pol', 'review_sub']] = df['clean_review'].apply(
        lambda x: pd.Series(get_sentiment(x))
    )
    df[['listing_pol', 'listing_sub']] = df['clean_listing'].apply(
        lambda x: pd.Series(get_sentiment(x))
    )
    df.to_pickle(processed_data)
    print(f"Successfully analyzed sentiment!")
    print(f"Processed file saved to {processed_data}")

