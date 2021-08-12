import pandas as pd


def get_history_data_filename(currency: str, granularity: str):
    return f"fx_bot/his_data/{currency}_{granularity}.pkl"


def get_instrument_data_filename():
    return f"fx_bot/instrument_info/instruments.pkl"

