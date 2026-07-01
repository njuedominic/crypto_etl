from src.db_connect import get_db_connection


def create_table():
    """Creates the cryptocurrency data table in the PostgreSQL database if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS crypto_data (
        coin_id VARCHAR(50),
        name VARCHAR(100),
        symbol VARCHAR(10),
        rank INTEGER,
        price_usd NUMERIC,
        volume_24h_usd NUMERIC,
        market_cap_usd NUMERIC,
        percent_change_24h NUMERIC,
        extracted_at TIMESTAMP,
        market_cap_to_volume_ratio NUMERIC(18, 6),
        PRIMARY KEY (coin_id, extracted_at)
    );
    """

    conn = get_db_connection()
    if not conn:
        return False  # Return False if the connection failed
        
    # FIXED: Placed at the correct indentation level so it always executes
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            conn.commit()
            print("Table 'crypto_data' created successfully or already exists.")
            return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    finally:
        conn.close()


def load_data(df):
    """Loads the transformed DataFrame into the PostgreSQL database."""
    if df.empty:
        print("Dataframe is empty. No data to load into the database.")
        return False

    # FIXED: Ensure the table is verified/created before loading
    if not create_table():
        print("Aborting load phase because table creation failed.")
        return False

    conn = get_db_connection()
    if not conn:
        return False  # Return False if the connection failed

    try:
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                insert_query = """
                INSERT INTO crypto_data (coin_id, name, symbol, rank, price_usd, volume_24h_usd, market_cap_usd, percent_change_24h, extracted_at, market_cap_to_volume_ratio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (coin_id, extracted_at) DO NOTHING;
                """
                cursor.execute(insert_query, (
                    row['coin_id'], row['name'], row['symbol'], row['rank'],
                    row['price_usd'], row['volume_24h_usd'], row['market_cap_usd'],
                    row['percent_change_24h'], row['extracted_at'], row['market_cap_to_volume_ratio']
                ))
            conn.commit()
            print(f"Loaded {len(df)} records into the database.")
            return True
    except Exception as e:
        print(f"Error loading data into the database: {e}")
        return False
    finally:
        conn.close()