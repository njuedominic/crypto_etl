import sys
from src.extract import extract_coins_data
from src.transform import transform_data
from src.load import create_table, load_data

def run_pipeline():
    print("Starting the ETL pipeline for cryptocurrency data...")

    # Step 1: Extract
    raw_data = extract_coins_data()
    if not raw_data:
        print("No data extracted. Exiting the pipeline.")
        sys.exit(1)

    # Step 2: Transform
    transformed_df = transform_data(raw_data)
    if transformed_df.empty:
        print("Transformed DataFrame is empty. Exiting the pipeline.")
        sys.exit(1)

    # Step 3: Load
    load_data(transformed_df)

    print("Pipeline executed successfully!")

if __name__ == "__main__":
    run_pipeline()

