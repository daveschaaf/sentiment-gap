import spacy
from src.constants import MIN_CHAR_LENGTH

class TextProcessor():

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
        return [
            " ".join(self.filter_tokens(doc)) for doc in self.nlp.pipe(df.loc[:, column].astype(str).str.lower(), batch_size=500)
        ]

