import pandas as pd
import spacy
from src.constants import MIN_CHAR_LENGTH
from tqdm import tqdm
from src.analyze_sentiment import get_sentiment


class TextProcessor():
    CRITICAL_RATING_THRESHOLD = 3

    def __init__(self):
      self.nlp = spacy.load('en_core_web_sm')

    def filter_tokens(self, doc):
        """
        1. Removes stop words and punctuation
        2. Lemmatizes (converts 'burning' to 'burn')
        3. Filters for Nouns, Adjectives, and Verbs
        """
        return [
            token.lemma_ for token in doc if not token.is_stop and token.is_alpha and len(token.text) >= MIN_CHAR_LENGTH
        ]

    def nlp_text(self, text):
        """
        1. Lowercases
        2. Returns a processed string
        """

        if not text or not isinstance(text, str):
            return ""
        doc = self.nlp(text.lower())

        clean_tokens = self.filter_tokens(doc)
        return " ".join(clean_tokens)

    def nlp_column(self, df, column):
        texts = df[column].astype(str).str.lower()

        docs = self.nlp.pipe(
            tqdm(texts, total=len(texts), desc=f"Processing nlp column: {column}"),
            batch_size=500
        )

        return [
            " ".join(self.filter_tokens(doc))
            for doc in docs
        ]
    
    def analyze_sentiment(self, df):
        df = df.copy()

        review_scores = [
            get_sentiment(text)
            for text in tqdm( df['clean_review'], desc="Review sentiment" )
        ]
        df[['review_pol', 'review_sub']] = pd.DataFrame(review_scores, index=df.index)
        listing_scores = [
            get_sentiment(text)
            for text in tqdm(df['clean_listing'], desc="Listing sentiment")
        ]
        df[['listing_pol', 'listing_sub']] = pd.DataFrame(listing_scores, index=df.index)
        return df

    def add_metadata_word_count(self, df):
        df = df.copy()

        df['listing_word_count'] = df['product_listing'].fillna('').str.split().str.len()
        combined_review = df['title'].fillna('') + " " + df['text'].fillna('')
        df['review_word_count'] = combined_review.str.split().str.len()
        
        return df
    def mark_critical_reviews(self, df):
        df = df.copy()
        df['is_critical'] = df['rating'] <= self.CRITICAL_RATING_THRESHOLD
        return df
