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
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])

    # formating data
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["price"] = round(df["price"], 2)
    df["daily_returns"] = df["price"].pct_change()
    # formatting market caps and total volumes later
    return df


def create_charts(data):
    fig, ax = plt.subplots(5, figsize=(8, 12))
    fig.suptitle("Crypto market analysis dashboard")

    # Overall course developement
    ax[0].set_title("course developement")
    x = data["timestamp"]
    y = data["price"]
    ax[0].plot(x, y)

    # highest course
    ax[1].set_title("Highest course")
    ax[1].axis("off")
    max_course = max(data["price"])
    ax[1].text(**style_text_card(max_course))

    # lowest course
    ax[2].set_title("Lowest course")
    ax[2].axis("off")
    min_course = min(data["price"])
    ax[2].text(**style_text_card(min_course))

    ax[3].set_title("Average")
    ax[3].axis("off")
    avg_course = round(sum(data["price"]) / len(data["price"]), 2)
    ax[3].text(**style_text_card(avg_course))

    # daily returns in barchart
    # TODO: when time grain is set to hourly(default), still only show daily returns
    ax[4].set_title("Daily returns")
    ax[4].stem(data["timestamp"], data["daily_returns"])

    plt.tight_layout()
    plt.show()


def style_text_card(text):
    return {
        "x": 0.5,
        "y": 0.6,
        "s": text,  # displayed number
        "fontsize": 48,
        "fontweight": "bold",
        "ha": "center",
        "va": "center",
        "color": "#1f77b4",
    }


if __name__ == "__main__":
    data = fetch_data(coin="bitcoin")
    create_charts(data)
