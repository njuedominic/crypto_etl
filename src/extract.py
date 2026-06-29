import requests

COIN_IDS = [
    "btc-bitcoin",
    "eth-ethereum",
    "sol-solana",
    "doge-dogecoin",
    "usdt-tether"
]

def extract_coins_data():
    extracted_data = []
    for coin_id in COIN_IDS:
        url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
        response = requests.get(url)
        if response.status_code == 200:
            coin_data = response.json()
            extracted_data.append(coin_data)
        else:
            print(f"Failed to fetch data for {coin_id}. Status code: {response.status_code}")
    return extracted_data

raw_data = extract_coins_data()
print(f"\nRetrieved {len(raw_data)} records.")
print(list(raw_data[0].keys()))
