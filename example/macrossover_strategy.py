import sys

import pandas as pd
import plotly.graph_objects as go

sys.path.append("/Users/chouwilliam/fx_bot")

import instrument
import utils

"""
MA Strategy
"""
currency = "CAD_CHF"
granularity = "H1"

ma_list = [50, 100]
i_currency = instrument.Instrument.get_instrument_by_name(currency)

df = pd.read_pickle(utils.get_history_data_filename(currency, granularity))
non_cols = ["time", "volume"]
mod_col = [x for x in df.columns if x not in non_cols]  # get the columns not in non_cols
df[mod_col] = df[mod_col].apply(pd.to_numeric)

df_ma = df[["time", "mid_o", "mid_h", "mid_l", "mid_c"]].copy()
for ma in ma_list:
    df_ma[f"MA_{ma}"] = df_ma.mid_c.rolling(window=ma).mean()
df_ma.dropna(inplace=True)
df_ma.reset_index(drop=True, inplace=True)


"""
define crossover/ crossunder trade signal
"""

df_ma["DIFF"] = df_ma.MA_50 - df_ma.MA_100
df_ma["DIFF_PREV"] = df_ma.DIFF.shift(1)


# df_ma.dropna(inplace=True)  # onle take the none na


# print(df_ma[["time", "mid_c", "MA_16", "MA_32", "DIFF", "DIFF_PREV"]])


def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:  # crossunder
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:  # crossover
        return -1
    return 0


df_ma["IS_TRADE"] = df_ma.apply(is_trade, axis=1)  # apple all the Data in the certain function
df_trades = df_ma[df_ma.IS_TRADE != 0].copy()
# print(df_trades)
print(f"Trade Number: {df_trades.shape[0]}")

"""
Access the performance !!
"""

df_trades["DELTA"] = (df_trades.mid_c.diff() / i_currency.pipLocation).shift(-1)

# gain

df_trades["GAIN"] = df_trades["DELTA"] * df_trades["IS_TRADE"]
df_trades["GAIN"].sum()

print(df_trades["GAIN"].sum())

"""
use plotly on bars
"""

df_plot = df_ma.iloc[-200:].copy()

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
for ma in ma_list:
    col = f"MA_{ma}"
    fig.add_trace(
        go.Scatter(
            x=df_plot.time, y=df_plot[col], line=dict(width=2), line_shape="spline", name=col,
        )
    )
fig.update_layout(
    width=1500,
    height=1000,
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
