import pandas as pd
import requests

# API DEMO

API_KEY = "5d475a6ef1636c3f21c5beae4106ec71-e7dd38f032059393592c6da22df7857e"
accountID = "101-011-6626734-003"
OANDA_URL = "https://api-fxpractice.oanda.com/v3"

SECURE_HEADER = {"Authorization": f"Bearer {API_KEY}"}

session = requests.Session()

instrument_data = pd.read_pickle("fx_bot/instrument_info/instruments.pkl")

currency = ["EUR", "USD", "GBP", "JPY", "CHF", "NZD", "CAD"]

k = "D"


def get_candles(pair_name: str, count: int, granularity: str):
    url = f"{OANDA_URL}/instruments/{pair_name}/candles"
    params = dict(count=count, granularity=granularity, price="MBA")
    response = session.get(url, params=params, headers=SECURE_HEADER)
    return response.status_code, response.json()


def get_candles_DataFrame(json_response):
    """get the vandle and turn into Data Frame

    Args:
        use the double loop to capture the bar data
        exclude the incomplete bar

    """
    prices = ["mid", "bid", "ask"]
    ohlc = ["o", "h", "l", "c"]
    our_data = []
    for candle in json_response["candles"]:
        if candle["complete"] == False:
            continue
        new = {}
        new["time"] = candle["time"]
        new["volume"] = candle["volume"]
        for price in prices:
            for oh in ohlc:
                new[f"{price}_{oh}"] = candle[price][oh]
        our_data.append(new)
    return pd.DataFrame.from_dict(our_data)


def save_file(candles_df, pair, granularity):
    candles_df.to_pickle(f"fx_bot/his_data/{pair}_{granularity}.pkl")


def create_data(pair, granularity):
    code, json_data = get_candles(pair, 5000, granularity)
    # check if status is 200
    if code != 200:
        print(pair, "Error in API")
        return
    df = get_candles_DataFrame(json_data)
    print(f"{pair} loaded {df.shape[0]} candles from {df.time.min()} to {df.time.max()}")
    save_file(df, pair, granularity)


# create all the possible cross pairs in FX

"""
get the combination of FX pairs list
"""
# print(instrument_data.name.unique())
# loaded all the data!
for p1 in currency:
    for p2 in currency:
        pair = f"{p1}_{p2}"
        # eliminate the same pairs like GBP_GBP
        if pair in instrument_data.name.unique():
            create_data(pair, k)
