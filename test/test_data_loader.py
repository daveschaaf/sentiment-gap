from src.data_loader import load_raw, process_reviews, clean_metadata, add_metadata_word_count
import pandas as pd

health_reviews = 'Health_and_Personal_Care.jsonl.gz'
def test_load_raw():
    limit = 10
    df = load_raw(health_reviews, limit=limit)
    expected_columns = ['rating', 'title', 'text', 'images', 'asin', 'parent_asin',
                         'user_id', 'timestamp', 'helpful_vote', 'verified_purchase']
    df_columns = df.columns
    for column in expected_columns:
        assert column in df_columns

def test_process_reviews():
    df = process_reviews(health_reviews, 2)
    assert len(df) == 2
    assert 'images'not in df.columns
    assert df.loc[0, 'review_image_count'] == 0
    assert df['text'].isnull().sum() == 0
    assert df['rating'].isnull().sum() == 0
    assert df['helpful_vote'].isnull().sum() == 0
    assert df['product_title'].isnull().sum() == 0

def test_clean_metadata(sample_meta_df):
    df = clean_metadata(sample_meta_df)

    for col in ['parent_asin', 'description', 'product_title', 'features',
                'rating_number', 'average_rating', ]:
        assert col in df.columns
        assert df[col].isnull().sum() == 0
    assert df.loc[0, 'listing_image_count'] == 1
    assert df.loc[0, 'listing_video_count'] == 2
    assert df.loc[0, 'listing_media_count'] == 3

def test_metadata_word_count():
    df = pd.DataFrame(
        [['This product is made of sand.', 'I love sand!', 'SAND!']], 
        columns=['product_listing', 'text', 'title']
    )
    df = add_metadata_word_count(df)
    """It adds the word count of the description"""
    assert df.loc[0, 'listing_word_count']== 6
    """It adds the word count of the review"""
    assert df.loc[0, 'review_word_count'] == 4

def test_product_listing(sample_meta_df):
    meta_df = clean_metadata(sample_meta_df)
    assert (meta_df['product_listing'].str.strip().str.len() < 10).sum() == 0
