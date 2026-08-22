import requests
import pandas as pd


def fetch_data(days=7):

    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

    params = {
        "vs_currency": "eur",
        "days": days,
        "interval": "daily"

    }

    #fetching the data
    response = requests.get(url, params)
    data = response.json()

    #loading into a data frame
    df = pd.DataFrame(
        {"timestamp": [x[0] for x in data["prices"]],
         "price": [x[1] for x in data["prices"]],
         "market_caps": [x[1] for x in data["market_caps"]],
         "total_volumes": [x[1] for x in data["total_volumes"]]
         }
    )

    #formating data
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["price"] = round(df["price"], 2)

    return df


if __name__ == "__main__":
    data = fetch_data()
    print(data)