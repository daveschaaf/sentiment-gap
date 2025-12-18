import pytest
import pandas as pd
import spacy
from src.nlp_utils import TextProcessor

@pytest.fixture(scope="session")
def text_processor():
    """
    Loads the SpaCy model via TextProcessor class once for the entire test session.
    """
    print("\n### Loading Spacy model... ###")
    return TextProcessor()

@pytest.fixture
def sample_meta_df():
    """Sample of meta data"""
    return pd.DataFrame({
        'parent_asin': ['asin1', 'asin2'],
        'description': ['test description', ['list', 'list description']],
        'title': ['', "Some Product Title" ],
        'features': [['feature1', 'feature2'],['better features', 'worse feature']]

    })

@pytest.fixture
def sample_review_df():
    """Mock of the user reviews."""
    return pd.DataFrame({
        'parent_asin': ['B001', 'B001', 'B002'],
        'text': ['Too strong!', 'Love the kick', 'Didnt work'],
        'rating': [1, 5, 2]
    })
