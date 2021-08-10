import pandas as pd
import requests

import api.defs as defs
import utils


class OandaAPI:
    def __init__(self):
        self.session = requests.Session()

    def fetch_instrument(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.accountID}/instruments"
        response = self.session.get(url, params=None, headers=defs.SECURE_HEADER)
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
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"
        params = dict(count=count, granularity=granularity, price="MBA")
        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)

        return response.status_code, response.json()


if __name__ == "__main__":
    api = OandaAPI()
    # print(api.fetch_candles("EUR_USD", 30, "M15"))
    # print(api.fetch_instrument())
    # df = api.get_instrument_df()
    api.save_instrument()
    # print(df)
