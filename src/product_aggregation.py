import pandas as pd

def aggregate_by_parent_asin(df, min_reviews = 5):
    agg_map = {}
    agg_map['rating'] = ['mean', 'std', 'count']
    agg_map['review_pol'] = ['mean', 'std']
    agg_map['review_sub'] = ['mean', 'std']
    agg_map['review_word_count'] = ['mean', 'std']
    for col in ['product_title', 'product_listing', 'listing_media_count',
                'listing_pol', 'listing_sub', 'listing_word_count',
                'rating_count']:
        agg_map[col] = ['first']

    agg_df: pd.DataFrame = df.groupby('parent_asin').agg(agg_map)
    agg_df.columns = ['_'.join(col) for col in agg_df.columns] # flatten columns

    return agg_df[agg_df['rating_count_first'] >= min_reviews].copy()

    
