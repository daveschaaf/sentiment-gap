import pandas as pd
import numpy as np

REVIEWS_RAW = 'data/raw/Health_and_Personal_Care.jsonl.gz'

def load_raw_jsonl(file_path, limit=10000):
    df = pd.read_json(file_path, lines=True, compression="gzip", nrows=limit)
    return pd.DataFrame(df)

def process_reviews(file_name, limit):
    df: pd.DataFrame = load_raw_jsonl(REVIEWS_RAW, limit=limit)

    # White list columns and set data types
    data_type_map = {
        'rating': 'float32',
        'title': 'string',
        'text': 'string',
        'asin': 'category',
        'parent_asin': 'category',
        'user_id': 'string',
        'helpful_vote': 'int32', 
        'verified_purchase': 'bool'
    }
    df = df.loc[:, list(data_type_map.keys())]
    df = df.astype({k: v for k, v in data_type_map.items()})
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # drop na for test or rating, and check for blanks
    df['text'] = df['text'].replace(r'^\s*$', np.nan, regex=True)
    df = df.dropna(subset=['text', 'rating'])

    # Fill tile and rating
    df['title'] = df['title'].fillna('No Title')
    df['helpful_vote'] = df['helpful_vote'].fillna(0)

    df.to_csv(file_name)
    return df
