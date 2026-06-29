from datetime import datetime
import pandas as pd

def transform_data(data):
    """Transforms the extracted cryptocurrency JSON data into a clean, structured pandas DataFrame."""

    if not data:
        print("No data provided to transform.")
        return pd.DataFrame()   # Returns an empty DataFrame if no data is provided
    
    print(f"Transforming data for {len(data)} coins.")
    flat_records = []

    for item  in data:

        # Extrcat fields from the root level and get the nested 'quotes' dictionary for USD

        usd_quotes = item.get('quotes', {}).get('USD', {})

        record = {
            'coin_id': item.get('id'),
            'name': item.get('name'),
            'symbol': item.get('symbol'),
            'rank': item.get('rank'),
            'price_usd': usd_quotes.get('price'),
            'volume_24h_usd': usd_quotes.get('volume_24h'),
            'market_cap_usd': usd_quotes.get('market_cap'),
            'percent_change_24h': usd_quotes.get('percent_change_24h'),
        }
        flat_records.append(record)

    # Create a DataFrame from the list of records
    df = pd.DataFrame(flat_records)

    # Convert numeric columns to appropriate data types
    numeric_columns = ["rank", "price_usd", "volume_24h_usd", "market_cap_usd", "percent_change_24h"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set errors to NaN

    # Add ingestion timestamp
    df['extracted_at'] = datetime.now()

    # Create a derived column: mmarket cap to vo;lume ratio
    df['market_cap_to_volume_ratio'] = df['market_cap_usd'] / df['volume_24h_usd']

    print("Transformation complete. DataFrame created.")
    return df

# Test the transformation function
if __name__ == "__main__":
    # Quick dummy test to verify logic runs without errors
    dummy_raw = [{
        "id": "btc-bitcoin", "name": "Bitcoin", "symbol": "BTC", "rank": 1,
        "quotes": {"USD": {"price": 60000.0, "volume_24h": 30000000.0, "market_cap": 1200000000.0, "percent_change_24h": 1.5}}
    }]
    transformed_df = transform_data(dummy_raw)
    print("\nSample transformed DataFrame columns and types:")
    print(transformed_df.dtypes)
    print("\nPreview:")
    print(transformed_df[["name", "price_usd", "market_cap_to_volume_ratio", "extracted_at"]])


