import sys

sys.path.append("/Users/chouwilliam/fx_bot")  # add this to fix the path problem
import pandas as pd
import requests
import shared.utils as utils
from account.api import API_KEY, OANDA_URL, SECURE_HEADER, accountID
from info.instrument import Instrument


class OandaAPI:
    def __init__(self):
        self.session = requests.Session()

    def fetch_instrument(self):
        url = f"{OANDA_URL}/accounts/{accountID}/instruments"
        response = self.session.get(url, params=None, headers=SECURE_HEADER)
        return response.status_code, response.json()

    def get_instrument_df(self):
        code, data = self.fetch_instrument()
        if code == 200:
            df = pd.DataFrame(data["instruments"])
            return df[["name", "type", "displayName", "pipLocation", "marginRate"]]
        else:
            return None

    def save_instrument(self):
        df = self.get_instrument_df()
        if df is not None:
            df.to_pickle(utils.get_instrument_data_filename())

    def fetch_candles(self, pair_name: str, count: int, granularity: str):
        url = f"{OANDA_URL}/instruments/{pair_name}/candles"
        params = dict(count=count, granularity=granularity, price="MBA")
        response = self.session.get(url, params=params, headers=SECURE_HEADER)

        return response.status_code, response.json()


if __name__ == "__main__":
    api = OandaAPI()
    # print(fetch_candles("EUR_USD", 30, "M15"))
    # print(fetch_instrument())
    df = Instrument.get_instrument_df()
    # save_instrument()
    print(df)
