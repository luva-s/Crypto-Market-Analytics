from api_client import fetch_data
from visualization import create_charts


def main():
    try:
        data = fetch_data(coin="bitcoin")
        create_charts(data)
    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()

