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
    max_course = data["price"].idxmax()
    max_course_date = data.loc[max_course, "timestamp"]
    ax[1].text(0.5, 0.5, f"Max: {data.loc[max_course, 'price']}\n{max_course_date}", ha="center", va="center", fontsize=24, color="#1f77b4")

    # lowest course
    ax[2].set_title("Lowest course")
    ax[2].axis("off")
    min_course = data["price"].idxmin()
    min_course_date = data.loc[min_course, "timestamp"]
    print(min_course_date)
    ax[2].text(0.5, 0.5, f"Min: {data.loc[min_course, 'price']}\n{min_course_date}", ha="center", va="center", fontsize=24, color="#1f77b4")

    ax[3].set_title("Average")
    ax[3].axis("off")
    avg_course = round(sum(data["price"]) / len(data["price"]), 2)
    ax[3].text(0.5, 0.5, f"Avg: {avg_course}", ha="center", va="center", fontsize=24, color="#1f77b4")

    # daily returns in barchart
    # TODO: when time grain is set to hourly(default), still only show daily returns
    ax[4].set_title("Daily returns")
    ax[4].stem(data["timestamp"], data["daily_returns"])

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    data = fetch_data(coin="bitcoin")
    create_charts(data)

