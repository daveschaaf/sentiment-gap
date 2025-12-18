from src.data_loader import process_reviews
from src.nlp_utils import TextProcessor
from pathlib import Path

def data_pipeline(file_name, base_dir="."):
    print(f"### Starting data pipeline for {file_name}")
    df = process_reviews(file_name, limit=10000, base_dir=base_dir)
    processor = TextProcessor()

    print("- Cleaning listings...")
    df.loc[:, 'clean_listing'] = processor.nlp_column(df, 'product_listing')
    print("- Cleaning reviews...")
    df.loc[:, 'clean_review'] = processor.nlp_column(df, 'text')
    
    cleaned_file_name = file_name.lower().replace(".jsonl.gz", "")
    output_path = Path(base_dir, "data", "processed", f"{cleaned_file_name}.pkl")
    df.to_pickle(output_path)
    
    print(f"Successfully saved cleaned file to:\n{output_path}")
    


if __name__ == "__main__":
    data_pipeline('Health_and_Personal_Care.jsonl.gz')
