import pandas as pd
import numpy as np
from pathlib import Path

def load_raw(file_name, limit=9999999):
    file_path = Path("data", 'raw', file_name)
    df = pd.read_json(file_path, lines=True, compression="gzip", nrows=limit)
    return pd.DataFrame(df)

def process_reviews(file_name, limit):
    df: pd.DataFrame = load_raw(file_name, limit=limit)

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

    raw_meta_df = load_raw(f"meta_{file_name}")
    meta_df = clean_metadata(raw_meta_df) 
    # Join with meta file
    df = df.merge(meta_df[['parent_asin', "product_title", "description", "features", 'product_listing']], on='parent_asin', how= 'left' )

    processed_file_path = Path('data', 'processed', file_name)
    df.to_csv(processed_file_path)
    return df

def clean_metadata(meta_df):

    meta_data_types = {
        'parent_asin': 'category',
        'title': 'string',
        'description': 'string', 
        'features': 'string'
    }
    meta_df = meta_df.dropna(subset=['parent_asin'])
    meta_df = meta_df.loc[:, list(meta_data_types.keys())]

    # convert lists to string
    for col in ['description', 'features']:
        meta_df[col] = meta_df[col].apply(lambda c: " ".join(c) if isinstance(c, list) else c)
    meta_df = meta_df.astype({k: v for k, v in meta_data_types.items()})

    # clean HTMl of tags
    meta_df['description'] = meta_df['description'].replace(r'<[^>]*>', '', regex=True)

    # Fill NA values with blank
    meta_df['description'].fillna('')
    meta_df['title'].fillna('')
    meta_df['features'].fillna('')

    meta_df['product_listing'] = f"""{meta_df['title']} {meta_df['description']} {meta_df['features']}""".strip()

    meta_df = meta_df.rename(columns={'title': 'product_title'})

    return pd.DataFrame(meta_df)
