import pyscopg2
from src.db_connect import get_db_connection


def create_table():
    """Creates the cryptocurrency data table in the PostgreSQL database if it doesn't exist."""
    create_table_querry = """
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
        
        try:
           with conn.cursor() as cursor:
                cursor.execute(create_table_querry)
                conn.commit()
                print("Table 'crypto_data' created successfully or already exists.")
                return True
        except Exception as e:
            print(f"Error creating table: {e}")
            return False
        finally:
            conn.close()
    else:
        print("Failed to connect to the database. Table creation aborted.")