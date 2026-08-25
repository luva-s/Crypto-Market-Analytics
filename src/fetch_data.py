import requests
import pandas as pd
import matplotlib.pyplot as plt



def fetch_data(days=7, coin="bitcoin", timegrain="hourly"):

    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

    params = {
        "vs_currency": "eur",
        "days": days,
        "interval": timegrain

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
    #formatting market caps and total volumes later 

    return df


if __name__ == "__main__":
    data = fetch_data(coin="solana")

    x = data["timestamp"]
    y = data["price"] 

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()