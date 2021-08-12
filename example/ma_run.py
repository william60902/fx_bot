import sys

import pandas as pd

import ma_result

sys.path.append("/Users/chouwilliam/fx_bot")  # add this to fix the path problem

import shared.utils as utils
from info.instrument import Instrument

pd.set_option("display.max_columns", None)  # print data with no ... to ignore


class BarConfigs:
    currency = "EUR_USD"
    currencies = "GBP, EUR, USD, CAD, JPY, NZD, CHF"  # [EUR_USD]
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
    price_data["IS_TRADE"] = price_data.apply(is_trade, axis=1)

    # grab the data that occur trades
    df_trades = price_data[price_data.IS_TRADE != 0].copy()
    df_trades["DELTA"] = (df_trades.mid_c.diff() / i_pair.pipLocation).shift(-1)
    df_trades["GAIN"] = df_trades["DELTA"] * df_trades["IS_TRADE"]

    print(
        f"{i_pair.name} {mashort} {malong} trades:{df_trades.shape[0]} gain: {df_trades.GAIN.sum():.0f}"
    )

    return ma_result.MAResult(
        df_trades=df_trades, currency=i_pair.name, params={"mashort": mashort, "malong": malong}
    )


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


def get_test_pairs(pair_str):
    existing_pairs = Instrument.get_instrument_dict().keys()
    # print(existing_pairs)
    pairs = pair_str.split(",")
    # print(pairs)  # ['GBP', ' EUR', ' USD', ' CAD', ' JPY', ' NZD', ' CHF']

    test_list = []
    for p1 in pairs:
        for p2 in pairs:
            p = f"{p1}_{p2}"
            # eliminate the same pairs like GBP_GBP
            if p in existing_pairs:
                test_list.append(p)
    print(test_list)
    return test_list


def process_results(results):
    results_list = [r.result_ob() for r in results]
    final_df = pd.DataFrame.from_dict(results_list)

    # check
    print(final_df.info())  # form is break
    print(final_df.head())


def run():

    currency = BarConfigs.currencies
    granularity = BarConfigs.granularity
    ma_short = [8, 6, 36, 64]
    ma_long = [32, 64, 96, 128, 256]
    i_pair = Instrument.get_instrument_dict()[pairname]

    price_data = get_price_data(currency, granularity)
    price_data = process_data(ma_short, ma_long, price_data)

    results = []

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong:
                continue

            results.append(evaluate_currency(i_pair, _mashort, _malong, price_data.copy()))
    process_results(results)


if __name__ == "__main__":
    # run()
    get_test_pairs("GBP, EUR, USD, CAD, JPY, NZD, CHF")
