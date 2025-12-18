import pytest
from src.nlp_utils import preprocess_text


@pytest.fixture
def sample_texts():
    return {
        'stop_words': ("Some noone the of on TEXT.", 'text'),
        'lowercase': ("THE BROWN FOX JUMP DOG", "brown fox jump dog"),
        'lemma': ("Dog is </br>sleeping", "dog sleep"),
        'filter': ("troll lives under the bridge of doom", "troll life bridge doom"),
        'empty': ("", "")
    }

def test_preprocess_text(sample_texts):
    """
    1. Lowercases ✅
    2. Removes stop words and punctuation
    3. Lemmatizes (converts 'burning' to 'burn')
    4. Filters for Nouns, Adjectives, and Verbs
    5. Returns a processed string
    """
    
    for case, (raw, expected) in sample_texts.items():
        assert preprocess_text(raw) == expected, case 
