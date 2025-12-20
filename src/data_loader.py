import pandas as pd
import numpy as np
from pathlib import Path
from src.constants import REVIEW_DATA_TYPES, META_DATA_TYPES

def load_raw(file_name, limit=9999999, base_dir="."):
    file_path = Path(base_dir, "data", 'raw', file_name)
    df = pd.read_json(file_path, lines=True, compression="gzip", nrows=limit)
    return pd.DataFrame(df)

def process_reviews(file_name, limit, base_dir="."):
    df: pd.DataFrame = load_raw(file_name, limit=limit, base_dir=base_dir)

    # White list columns and set data types
    df = df.loc[:, list(REVIEW_DATA_TYPES.keys())]
    df = df.astype({k: v for k, v in REVIEW_DATA_TYPES.items()})
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # drop na for test or rating, and check for blanks
    df['text'] = df['text'].replace(r'^\s*$', np.nan, regex=True)
    df = df.dropna(subset=['text', 'rating'])

    # Fill tile and rating
    df['title'] = df['title'].fillna('No Title')
    df['helpful_vote'] = df['helpful_vote'].fillna(0)
    
    df['review_image_count'] = df.loc[:, 'images'].str.len()
    df = df.drop(columns=['images'])

    raw_meta_df = load_raw(f"meta_{file_name}", base_dir=base_dir)
    meta_df = clean_metadata(raw_meta_df) 
    # Join with meta file
    df = df.merge(meta_df[['description', 'product_title', 'product_listing', 'features',
                           'average_rating','rating_number', 'parent_asin']], on='parent_asin', how= 'left' )

    return df

def clean_metadata(meta_df):

    meta_df = meta_df.dropna(subset=['parent_asin'])
    meta_df = meta_df.loc[:, list(META_DATA_TYPES.keys())]

    # convert lists to string
    for col in ['description', 'features']:
        meta_df[col] = meta_df[col].apply(lambda c: " ".join(c) if isinstance(c, list) else c)
    meta_df = meta_df.astype({k: v for k, v in META_DATA_TYPES.items()})

    # clean HTMl of tags
    meta_df['description'] = meta_df['description'].replace(r'<[^>]*>', '', regex=True)
    
    image_count = meta_df.loc[:, 'images'].str.len()
    video_count = meta_df.loc[:, 'videos'].str.len()
    meta_df.loc[:, 'listing_image_count'] = image_count
    meta_df.loc[:, 'listing_video_count'] = video_count
    meta_df.loc[:, 'listing_media_count'] = image_count + video_count

    meta_df = meta_df.drop(columns=['images', 'videos'])

    # Fill NA values with blank
    meta_df['description'].fillna('')
    meta_df['title'].fillna('')
    meta_df['features'].fillna('')

    meta_df['product_listing'] = (
        meta_df['title'] + " " +
        meta_df['description'] + " " +
        meta_df['features']
    ).str.strip()

    meta_df = meta_df.rename(columns={'title': 'product_title'})

    return pd.DataFrame(meta_df)

def add_metadata_word_count(df):
    df['listing_word_count'] = df['product_listing'].fillna('').str.split().str.len()
    combined_review = df['title'].fillna('') + " " + df['text'].fillna('')
    df['review_word_count'] = combined_review.str.split().str.len()
    
    return df
