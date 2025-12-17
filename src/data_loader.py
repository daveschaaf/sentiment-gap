import pandas as pd
import gzip
import json

REVIEWS_RAW = 'data/raw/Health_and_Personal_Care.jsonl.gz'

def load_reviews(path, limit=10000):
    df = pd.read_json(path, lines=True, compression="gzip", nrows=limit)
    return df

# dict_keys(['rating', 'title', 'text', 'images', 'asin', 'parent_asin', 'user_id', 'timestamp', 'helpful_vote', 'verified_purchase'])
