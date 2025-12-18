import pytest
import pandas as pd

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
