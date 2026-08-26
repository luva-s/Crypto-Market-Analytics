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

    # fetching the data
    response = requests.get(url, params)
    data = response.json()

    # loading into a data frame
    df = pd.DataFrame(
        {"timestamp": [x[0] for x in data["prices"]],
         "price": [x[1] for x in data["prices"]],
         "market_caps": [x[1] for x in data["market_caps"]],
         "total_volumes": [x[1] for x in data["total_volumes"]]
         }
    )

    # formating data
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["price"] = round(df["price"], 2)
    # formatting market caps and total volumes later

    return df


def create_charts(data):
    fig, ax = plt.subplots(4)
    fig.suptitle("Crypto market analysis dashboard")

    #Overall course developement
    ax[0].set_title("course developement")
    x = data["timestamp"]
    y = data["price"]
    ax[0].plot(x, y)

    #highest course 
    ax[1].set_title("Highest course")
    ax[1].axis("off")
    max_course = max(data["price"])
    ax[1].text(x=0.5,
               y=0.6,
               s= max_course, #displayed number
               fontsize=48,
               fontweight='bold',
               ha='center',
               va='center',
               color='#1f77b4',)

    #lowest course
    ax[2].set_title("Lowest course")
    ax[2].axis("off")
    min_course = min(data["price"])
    ax[2].text(x=0.5,
               y=0.6,
               s= min_course, #displayed number
               fontsize=48,
               fontweight='bold',
               ha='center',
               va='center',
               color='#1f77b4',)

    ax[3].set_title("Average")
    ax[3].axis("off")
    avg_course = round(sum(data["price"]) / len(data["price"]), 2)
    ax[3].text(x=0.5,
               y=0.6,
               s= avg_course, #displayed number
               fontsize=48,
               fontweight='bold',
               ha='center',
               va='center',
               color='#1f77b4',)
    plt.show()



if __name__ == "__main__":
    try: 
        data = fetch_data(coin="bitcoin")
        create_charts(data)
    except Exception: 
        print("somethin did not work")
