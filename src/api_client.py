import requests
import pandas as pd


def fetch_data(days=7, coin="bitcoin", timegrain="hourly"):

    # Input validation
    if days <= 0:
        raise ValueError("days must be a positive integer")
    if not isinstance(coin, str) or len(coin.strip()) == 0:
        raise ValueError("coin must be a non-empty string")
    valid_intervals = ["hourly", "daily"]
    if timegrain.lower() not in valid_intervals:
        raise ValueError(f"timegrain must be one of {valid_intervals}")

    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

    params = {
        "vs_currency": "eur",
        "days": days,
        "interval": timegrain.lower()
    }

    # fetching the data
    try:
        response = requests.get(url, params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}") 
        return

    # loading into a data frame
    data = response.json()
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])

    # formating data
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["price"] = df["price"].round(2)
    df["daily_returns"] = df["price"].pct_change()
    
    return df

