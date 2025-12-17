from src.data_loader import load_reviews, REVIEWS_RAW

def test_load_reviews():
    assert REVIEWS_RAW == 'data/raw/Health_and_Personal_Care.jsonl.gz'
    limit = 10
    df = load_reviews(REVIEWS_RAW, limit=limit)
    expected_columns = ['rating', 'title', 'text', 'images', 'asin', 'parent_asin', 'user_id', 'timestamp', 'helpful_vote', 'verified_purchase']
    df_columns = df.columns
    for column in expected_columns:
        assert column in df_columns
    assert len(df) == 10


