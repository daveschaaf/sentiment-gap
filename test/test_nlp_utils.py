import pytest
import pandas as pd
from src.nlp_utils import TextProcessor

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


def mock_get_sentiment(text):
    return (0.5, 0.25)

def test_analyze_sentiment(monkeypatch):

    df = pd.DataFrame({
        "clean_review": ["great product", "terrible experience"],
        "clean_listing": ["high quality item", "low quality item"]
    })
    processor = TextProcessor()
    monkeypatch.setattr(
        "src.nlp_utils.get_sentiment",
        mock_get_sentiment
    )
    result = processor.analyze_sentiment(df)

    """new columns do not exist in original"""
    assert "review_pol" not in df.columns
    assert "review_sub" not in df.columns
    assert "listing_pol" not in df.columns
    assert "listing_sub" not in df.columns

    """new columns exist"""
    expected_cols = {
        "review_pol", "review_sub",
        "listing_pol", "listing_sub"
    }
    assert expected_cols.issubset(result.columns)

    """new values exist"""
    
    assert (result["review_pol"] == 0.5).all()
    assert (result["review_sub"] == 0.25).all()
    assert (result["listing_pol"] == 0.5).all()
    assert (result["listing_sub"] == 0.25).all()
    
    """preserves the shape"""
    assert len(result) == len(df)

def test_add_metadata_word_count():
    df = pd.DataFrame({
        "product_listing": ["This is a product", None, "Another listing"],
        "title": ["Great", None, "Not bad"],
        "text": ["Amazing experience", "Needs improvement", None]
    })
    processor = TextProcessor()
    result = processor.add_metadata_word_count(df)

    assert 'listing_word_count' not in df.columns
    assert 'review_word_count' not in df.columns
    
    assert list(result['listing_word_count']) == [4,0,2]
    assert list(result['review_word_count']) == [3,2,2]

def test_mark_critical_reviews():
    processor = TextProcessor()
    
    nice_df = pd.DataFrame()
    nice_df['rating'] = [5]
    result = processor.mark_critical_reviews(nice_df)
    assert result.loc[0, 'is_critical'] == False
    
    crit_df = pd.DataFrame()
    crit_df['rating'] = [3]
    result = processor.mark_critical_reviews(crit_df)
    assert result.loc[0, 'is_critical'] == True
