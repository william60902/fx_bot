import pandas as pd
import requests

import api.defs as defs

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
url = f"{defs.OANDA_URL}/instruments/{instrument}/candles"

params = dict(count=count, granularity=granularity, price="MBA")

response = session.get(url, params=params, headers=defs.SECURE_HEADER)

# data manipulate

data = response.json()

# print(data.keys())

"""
dict_keys(['instrument', 'granularity', 'candles'])
"""


candles = data["candles"]

# print(candles)

# take the mid ohlcv data

# print(mid_bar)

mid_bar_data = []
for item in candles:
    new = dict(
        time=item["time"],
        open=item["mid"]["o"],
        high=item["mid"]["h"],
        low=item["mid"]["l"],
        close=item["mid"]["c"],
        volume=item["volume"],
    )
    mid_bar_data.append(new)
mid_bar_data = pd.DataFrame(mid_bar_data)

ask_bar_data = []
for item in candles:
    new = dict(
        time=item["time"],
        open=item["ask"]["o"],
        high=item["ask"]["h"],
        low=item["ask"]["l"],
        close=item["ask"]["c"],
        volume=item["volume"],
    )
    ask_bar_data.append(new)
ask_bar_data = pd.DataFrame(ask_bar_data)

bid_bar_data = []
for item in candles:
    new = dict(
        time=item["time"],
        open=item["bid"]["o"],
        high=item["bid"]["h"],
        low=item["bid"]["l"],
        close=item["bid"]["c"],
        volume=item["volume"],
    )
    bid_bar_data.append(new)
bid_bar_data = pd.DataFrame(bid_bar_data)


print(mid_bar_data)
