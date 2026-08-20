import requests

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin",
    "vs_currencies": "eur"
}
response = requests.get(url, params)
print(response.json())