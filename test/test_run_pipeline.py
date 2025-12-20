import pytest
import pandas as pd
from src.run_pipeline import data_pipeline
import os


def test_data_pipeline(tmp_path):
    """
    Integration test
    """
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    test_file = "health_test.jsonl.gz"
    df_mock = pd.DataFrame({
        'rating': [5.0],
        'title': ['Great'],
        'text': ['This mint is cooling.'],
        'parent_asin': ['B001'],
        'asin': ['B001-A'],
        'user_id': ['USER123'],
        'helpful_vote': [0],
        'verified_purchase': [True],
        'images': [[{'large': 'large_image location'},{"small": "small image location"}]]
    })
    df_mock.to_json(raw_dir / test_file, orient='records',lines=True, compression='gzip')

    meta_file = f"meta_{test_file}"
    meta_mock = pd.DataFrame({
        'parent_asin': ['B001'],
        'title': ['Minty Fresh'],
        'description': [['Best mints ever.']],
        'features': [['Cooling effect']],
        'average_rating': '3.7',
        'rating_number': "739",
        'images': [[{"large": "large_image_location", "small": "small_image_location"}]],
        'videos': [[{"title": 'video_title', "url": 'video_url'}]]
    })
    meta_mock.to_json(raw_dir / meta_file, orient='records', lines=True, compression='gzip')

    data_pipeline(test_file, base_dir=tmp_path)

    saved_pickle = processed_dir / "health_test.pkl"
    assert os.path.exists(saved_pickle)
    reload = pd.read_pickle(saved_pickle)
    assert reload.loc[0, 'clean_review'] == "mint cool"
    assert reload.loc[0, 'clean_listing'] == "minty fresh good mint cool effect"
    assert reload.loc[0, 'listing_word_count'] == 7
    assert reload.loc[0, 'review_word_count'] == 5


