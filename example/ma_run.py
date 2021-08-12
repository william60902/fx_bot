import sys

import pandas as pd

sys.path.append("/Users/chouwilliam/fx_bot")  # add this to fix the path problem

import shared.utils as utils
from info.instrument import Instrument

pd.set_option("display.max_columns", None)  # print data with no ... to ignore


class BarConfigs:
    currency = "EUR_USD"
    granularity = "H1"


def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:  # crossunder
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:  # crossover
        return -1
    return 0


def get_ma_col(ma):
    # just get the name
    return f"MA_{ma}"


def evaluate_currency(i_pair, mashort, malong, price_data):
    price_data["DIFF"] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data["DIFF_PREV"] = price_data.DIFF.shift(1)
    price_data["IS_TRADE"] = price_data(is_trade, axis=1)

    # grab the data that occur trades
    df_trades = price_data[price_data.IS_TRADE != 0].copy()
    df_trades["DELTA"] = (df_trades.mid_c.diff() / i_pair.pipLocation).shift(-1)
    df_trades["GAIN"] = df_trades["DELTA"] * df_trades["IS_TRADE"]

    # print(f"{i_pair.name}{mashort}{malong} trades:{df_trades.shape[0]} gain: {df_trades["GAIN"].sum():.0f}")

    return df_trades["GAIN"].sum()


def get_price_data(currency: str, granularity):
    df = pd.read_pickle(utils.get_history_data_filename(currency, granularity))

    # change data str into float
    non_cols = ["time", "volume"]
    mod_col = [x for x in df.columns if x not in non_cols]
    df[mod_col] = df[mod_col].apply(pd.to_numeric)

    return df[["time", "mid_o", "mid_h", "mid_l", "mid_c"]]


def process_data(ma_short: list, ma_long: list, price_data):
    #  making unique
    ma_list = set(ma_short + ma_long)

    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()

    return price_data


def run():

    currency = BarConfigs.currency
    granularity = BarConfigs.granularity
    ma_short = [8, 6, 36, 64]
    ma_long = [32, 64, 96, 128, 256]
    i_pair = Instrument.get_instrument_dict()[currency]

    price_data = get_price_data(currency, granularity)
    price_data = process_data(ma_short, ma_long, price_data)

    best = -1000000.0
    b_mashort = 0
    b_malong = 0

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong:
                continue

            res = evaluate_currency(i_pair, _mashort, _malong, price_data.copy())
            if res > best:
                best = res
                b_mashort = _mashort
                b_malong = _malong
    print(f"Best:{best}, MASHORT:{b_mashort}, MASHORT: {b_malong}")


if __name__ == "__main__":
    run()
