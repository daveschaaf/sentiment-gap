import pytest
import pandas as pd

@pytest.fixture
def sample_texts():
    return {
        'stop_words': ("Some noone the of on TEXT.", 'text'),
        'lowercase': ("THE BROWN FOX JUMP DOG", "brown fox jump dog"),
        'lemma': ("Dog is </br>sleeping", "dog sleep"),
        'filter': ("troll lives under the bridge of doom", "troll life bridge doom"),
        'empty': ("", "")
    }
@pytest.fixture
def sample_data_frame():
    data = [
        ["My dog wants to go outside", "dog want outside"],
        ["I need to do homework.", "need homework"]
    ]
    return pd.DataFrame(data, columns= ('text', 'expectation'))

def test_nlp_text(text_processor, sample_texts):
    """
    1. Lowercases
    2. Removes stop words and punctuation
    3. Lemmatizes (converts 'burning' to 'burn')
    4. Filters for Nouns, Adjectives, and Verbs
    5. Returns a processed string
    """
    
    for case, (raw, expected) in sample_texts.items():
        assert text_processor.nlp_text(raw) == expected, case

def test_nlp_column(text_processor, sample_data_frame):
    """
    Test  the same filtering logic works for a column
    """
    result = text_processor.nlp_column(sample_data_frame, 'text')
    assert result[0] == sample_data_frame.loc[0, 'expectation']
    assert result[1] == sample_data_frame.loc[1,'expectation']
