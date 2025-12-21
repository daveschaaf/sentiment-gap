import pandas as pd
from src.product_aggregation import aggregate_by_parent_asin
import pytest

def test_aggregate_by_parent_asin():
    df = pd.DataFrame()
    asin = 'BEETASIN'
    df['parent_asin'] = [asin]
    df['product_title'] = ['Beet Juice']
    df['product_listing'] = ["Beet Juice 100% pure beet, all juice"]
    df['listing_media_count'] = [3]
    df['listing_pol'] = 0.1
    df['listing_sub'] = 0.2
    df['listing_word_count'] = 9
    rv1 = df.copy()
    rv2 = df.copy()

    rv1['title'] = ['I like beets']
    rv1['text'] = ['Seriously, these beets were the best']
    rv1['rating'] = 5
    rv1['timestamp'] = pd.to_datetime('2025-03-31')
    rv1['helpful_vote'] = 101
    rv1['image_count'] = 1
    rv1['review_pol'] = 0.8
    rv1['review_sub'] = 0.8
    rv1['review_word_count'] = 9
    agg_rv1_df = aggregate_by_parent_asin(rv1, min_reviews=2)

    assert asin not in agg_rv1_df.index
    assert agg_rv1_df.empty

    rv2['title'] = ['HATED beets']
    rv2['text'] = ['terrible awful!']
    rv2['rating'] = 1
    rv2['timestamp'] = pd.to_datetime('2025-02-04')
    rv2['helpful_vote'] = 10
    rv2['image_count'] = 0
    rv2['review_pol'] = -0.5
    rv2['review_sub'] = 0.2
    rv2['review_word_count'] = 4

    combined_df = pd.concat([rv1, rv2], ignore_index=True)

    agg_df = aggregate_by_parent_asin(combined_df, min_reviews=2)
    assert len(agg_df) == 1
    assert agg_df.index.name == 'parent_asin'
    assert asin in agg_df.index

    """keeps all the listing level information"""
    included_cols = list(df.columns.copy())
    included_cols.remove('parent_asin')
    for col in included_cols:
        assert agg_df.loc[asin, f"{col}_first"] == df.loc[0, col], str(col)

    """aggregates the review level information"""
    assert agg_df.loc[asin, 'rating_mean'] == 3
    assert agg_df.loc[asin, 'rating_std'] == pytest.approx(2.828, abs=1e-3)
    assert agg_df.loc[asin, 'rating_count'] == 2
    assert agg_df.loc[asin, "review_pol_mean"] == pytest.approx(0.15, abs=1e-3)
    assert agg_df.loc[asin, "review_pol_std"] == pytest.approx(0.919, abs=1e-3)
    assert agg_df.loc[asin, "review_sub_mean"] == 0.5
    assert agg_df.loc[asin, "review_sub_std"] == pytest.approx(0.424, abs=1e-3)
    assert agg_df.loc[asin, 'review_word_count_mean'] == 6.5
    assert agg_df.loc[asin, 'review_word_count_std'] == pytest.approx(3.535, abs=1e-3)


