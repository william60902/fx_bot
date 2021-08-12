import sys

import pandas as pd
import plotly.graph_objects as go

sys.path.append("/Users/chouwilliam/fx_bot")  # add this to fix the path problem

import shared.utils as utils
from account.api import API_KEY, OANDA_URL, SECURE_HEADER, accountID

"""
Firtly we need to change the ohlc data from str into float
"""


pair = "EUR_USD"
granularity = "H1"

df = pd.read_pickle(utils.get_history_data_filename(pair, granularity))

# print(df.describe())

# print(df.head())

# only time and volume are float

non_cols = ["time", "volume"]

mod_col = [x for x in df.columns if x not in non_cols]  # get the columns not in non_cols

# print(mod_col)

"""
convert into float from str
"""

df[mod_col] = df[mod_col].apply(pd.to_numeric)

# print(df.describe())

# done! all the bar data convert into float

"""
use plotly on bars
"""

df_plot = df.iloc[-100:].copy()

# print(df_plot.shape)

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df_plot.time,
        open=df_plot.mid_o,
        high=df_plot.mid_h,
        low=df_plot.mid_l,
        close=df_plot.mid_c,
        line=dict(width=1),
        opacity=1,
        increasing_fillcolor="#24A06B",
        decreasing_fillcolor="#CC2E3C",
        increasing_line_color="#2EC886",
        decreasing_line_color="#FF3A4C",  # make the color more bright
    )
)

fig.update_layout(
    width=1500,
    height=700,
    margin=dict(l=10, b=10, t=10),
    font=dict(size=10, color="#e1e1e1"),
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
)  # height widgt

fig.update_xaxes(
    gridcolor="#1f292f", showgrid=True, fixedrange=True, rangeslider=dict(visible=False)
)

fig.update_yaxes(gridcolor="#1f292f", showgrid=True)

fig.show()
