import pandas as pd
from src.data_loader import load_reviews
from src.nlp_utils import TextProcessor
from pathlib import Path
from src.product_aggregation import aggregate_by_parent_asin

def load_and_preprocess(file_name, limit=500000, base_dir="."):
    df = load_reviews(file_name, limit=limit, base_dir=base_dir)
    processor = TextProcessor()

    df.loc[:, 'clean_listing'] = processor.nlp_column(df, 'product_listing')
    df.loc[:, 'clean_review'] = processor.nlp_column(df, 'text')
    df = processor.analyze_sentiment(df)
    df = processor.add_metadata_word_count(df)
    df = processor.mark_critical_reviews(df)

    cleaned_file_name = file_name.lower().replace(".jsonl.gz", "")
    output_path = Path(base_dir, "data", "processed", f"{cleaned_file_name}.pkl")
    df.to_pickle(output_path)
    print(f"\n### Successfully saved cleaned file to:\n{output_path}")
    return df



if __name__ == "__main__":
    data_set = 'Health_and_Personal_Care.jsonl.gz'
    limit = 10000
    print(f"\n### Loading {limit} records from {data_set}...")
    df = load_and_preprocess(data_set, limit = limit)
    print(f"\n### Data loaded and preprocessed...")

    print(f"\n### Aggregating by parent_asin...")
    agg_df: pd.DataFrame = aggregate_by_parent_asin(df)
    if not agg_df.empty:
        print(f"\n### Products aggregated. {len(agg_df)} available...")
        clean_name = data_set.replace('.jsonl.gz', '').lower()
        output_path = Path("data", "processed", f"{clean_name}_products.pkl")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        agg_df.to_pickle(output_path)
        print(f"\n### Products saved to {output_path} ###")
    else:
        print("No products met min_reviews threshold.") 
