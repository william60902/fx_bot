import pandas as pd
import requests

from api.defs import OANDA_URL, SECURE_HEADER

session = requests.Session()

instrument = "EUR_USD"
count = 500
granularity = "D"
start = "2020-01-01"
end = "2021-08-01"

# To-Do add time/date control

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# for bar
url = f"{OANDA_URL}/instruments/{instrument}/candles"

params = dict(count=count, granularity=granularity, price="MBA")

response = session.get(url, params=params, headers=SECURE_HEADER)

# data manipulate

data = response.json()

# print(data.keys())

"""
dict_keys(['instrument', 'granularity', 'candles'])
"""
prices = ["mid", "bid", "ask"]
ohlc = ["o", "h", "l", "c"]


"""
use the double loop to capture the bar data

"""

our_data = []
for candle in data["candles"]:
    # Exclude the incomplete bar
    if candle["complete"] == False:
        continue
    new = {}
    new["time"] = candle["time"]
    new["volume"] = candle["volume"]
    for price in prices:
        for oh in ohlc:
            new[f"{price}_{oh}"] = candle[price][oh]
    our_data.append(new)


candle_data = pd.DataFrame.from_dict(our_data)

# print(candle_data)

"""
save as pickle
"""

candle_data.to_pickle("EUR_USD_H1.pkl")

test_df = pd.read_pickle("EUR_USD_H1.pkl")

print(test_df)
