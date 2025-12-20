from src.data_loader import process_reviews, add_metadata_word_count
from src.nlp_utils import TextProcessor
from pathlib import Path

def data_pipeline(file_name, limit=500000, base_dir="."):
    print(f"### Starting data pipeline for {file_name}")
    df = process_reviews(file_name, limit=limit, base_dir=base_dir)
    processor = TextProcessor()

    df.loc[:, 'clean_listing'] = processor.nlp_column(df, 'product_listing')
    df.loc[:, 'clean_review'] = processor.nlp_column(df, 'text')
    df = processor.analyze_sentiment(df)
    df = processor.add_metadata_word_count(df) 

    cleaned_file_name = file_name.lower().replace(".jsonl.gz", "")
    output_path = Path(base_dir, "data", "processed", f"{cleaned_file_name}.pkl")
    df.to_pickle(output_path)
    
    print(f"Successfully saved cleaned file to:\n{output_path}")
    return df



if __name__ == "__main__":
    df = data_pipeline('Health_and_Personal_Care.jsonl.gz', limit = 10)

    
