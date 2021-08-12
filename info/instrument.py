import sys

import pandas as pd

sys.path.append("/Users/chouwilliam/fx_bot")  # add this to fix the path problem

import shared.utils as utils


class Instrument:
    def __init__(self, ob):
        self.name = ob["name"]
        self.type = ob["type"]
        self.displayName = ob["displayName"]
        self.pipLocation = pow(10, ob["pipLocation"])  # -4 -> 0.0001
        # self.displayPrecision = ob["displayPrecision"]
        # self.tradeUnitsPrecision = ob["tradeUnitsPrecision"]
        # self.minimumTradeSize = ob["minimumTradeSize"]
        # self.maximumTrailingStopDistance = ob["maximumTrailingStopDistance"]
        # self.minimumTrailingStopDistance = ob["minimumTrailingStopDistance"]
        # self.maximumPositionSize = ob["maximumPositionSize"]
        # self.maximumOrderUnits = ob["maximumOrderUnits"]
        self.marginRate = ob["marginRate"]
        # self.guaranteedStopLossOrderMode = ob["guaranteedStopLossOrderMode"]
        # self.tags = ob["tags"]
        # self.financing = ob["financing"]

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def get_instrument_df(cls):
        return pd.read_pickle(utils.get_instrument_data_filename())

    @classmethod
    def get_instrument_list(cls):
        df = cls.get_instrument_df()
        return [Instrument(x) for x in df.to_dict(orient="records")]

    @classmethod
    def get_instrument_dict(cls):
        i_list = cls.get_instrument_list()
        i_keys = [x.name for x in i_list]
        return {k: v for (k, v) in zip(i_keys, i_list)}

    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instrument_dict()
        if pairname in d:
            return d[pairname]
        else:
            raise ValueError("The pairname is not in the list@")


# if __name__ == "__main__":
#     # print(Instrument.get_instrument_df())

#     df = Instrument.get_instrument_df()
#     # print(df.to_dict(orient="records"))
#     ll = df.to_dict(orient="records")

#     for item in ll:
#         print(item)

# if __name__ == "__main__":
#     print(Instrument.get_instrument_list())

if __name__ == "__main__":
    # for k, v in Instrument.get_instrument_dict().items():
    #     print(k, v)
    print(Instrument.get_instrument_by_name("EUR_USD"))

