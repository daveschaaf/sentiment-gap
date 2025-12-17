from src.data_loader import load_raw, process_reviews, clean_metadata
import os

health_reviews = 'Health_and_Personal_Care.jsonl.gz'
def test_load_raw():
    limit = 10
    df = load_raw(health_reviews, limit=limit)
    expected_columns = ['rating', 'title', 'text', 'images', 'asin', 'parent_asin', 'user_id', 'timestamp', 'helpful_vote', 'verified_purchase']
    df_columns = df.columns
    for column in expected_columns:
        assert column in df_columns

def test_process_reviews():
    processed_file = "data/processed/test_health_and_personal_care.csv"
    df = process_reviews(health_reviews, 100)
    assert len(df) == 100
    assert 'images'not in df.columns
    assert df['text'].isnull().sum() == 0
    assert df['rating'].isnull().sum() == 0
    assert df['helpful_vote'].isnull().sum() == 0
    assert df['product_title'].isnull().sum() == 0
    assert os.path.exists(processed_file)
    os.remove(processed_file)

def test_clean_metadata(sample_meta_df):
    test_meta_path = "meta_Health_and_Personal_Care.jsonl.gz"

    df = clean_metadata(sample_meta_df)

    for col in ['parent_asin', 'description', 'title', 'features']:
        assert col in df.columns
        assert df[col].isnull().sum() == 0

def test_product_listing(sample_meta_df):
    meta_df = clean_metadata(sample_meta_df)
    assert (meta_df['product_listing'].str.strip().str.len() < 10).sum() == 0
