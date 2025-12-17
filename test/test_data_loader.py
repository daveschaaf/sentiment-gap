from src.data_loader import load_raw_jsonl, REVIEWS_RAW, process_reviews
import os


def test_load_raw_jsonl():
    assert REVIEWS_RAW == 'data/raw/Health_and_Personal_Care.jsonl.gz'
    limit = 10
    df = load_raw_jsonl(REVIEWS_RAW, limit=10)
    expected_columns = ['rating', 'title', 'text', 'images', 'asin', 'parent_asin', 'user_id', 'timestamp', 'helpful_vote', 'verified_purchase']
    df_columns = df.columns
    for column in expected_columns:
        assert column in df_columns

    # df = load_reviews(REVIEWS_RAW, limit = 500000)
    # assert len(df) == 494121
def test_process_reviews():
    processed_file = "data/processed/test_health_and_personal_care.csv"
    df = process_reviews(processed_file, 10)
    assert len(df) == 10
    assert 'images'not in df.columns
    assert os.path.exists(processed_file)
    os.remove(processed_file)


