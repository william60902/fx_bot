import json

import pandas as pd
import requests

from api.defs import API_KEY, OANDA_URL, SECURE_HEADER, accountID

session = requests.Session()


# for account summary
url = f"{OANDA_URL}/accounts/{accountID}/instruments"
# print(url)

response = session.get(url, params=None, headers=SECURE_HEADER)

# print(response.status_code)  # Check the API whether is 200

# data = requests.get(url).json()

data = response.json()
# print(response.json())

# print(data.keys())

"""
dict_keys(['instruments', 'lastTransactionID'])
"""

instruments = data["instruments"]

# print(len(instruments)) = 124 tradeable info

instruments[0].keys()

"""
dict_keys(['name', 'type', 'displayName', 'pipLocation', 'displayPrecision', 
'tradeUnitsPrecision', 'minimumTradeSize', 'maximumTrailingStopDistance', 'minimumTrailingStopDistance', 
'maximumPositionSize', 'maximumOrderUnits', 'marginRate', 'guaranteedStopLossOrderMode', 'tags', 'financing'])

"""

# make an instrument info list

instruments_info = []

for item in instruments:
    new = dict(
        name=item["name"],
        type=item["type"],
        displayName=item["displayName"],
        pipLocation=item["pipLocation"],
        # displayPrecision=item["displayPrecision"],
        # tradeUnitsPrecision=item["tradeUnitsPrecision"],
        # minimumTradeSize=item["minimumTradeSize"],
        # maximumTrailingStopDistance=item["maximumTrailingStopDistance"],
        # minimumTrailingStopDistance=item["minimumTrailingStopDistance"],
        # maximumPositionSize=item["maximumPositionSize"],
        # maximumOrderUnits=item["maximumOrderUnits"],
        marginRate=item["marginRate"],
        # guaranteedStopLossOrderMode=item["guaranteedStopLossOrderMode"],
        # tags=item["tags"],
        # financing=item["financing"],
    )
    instruments_info.append(new)
# instruments_info = pd.DataFrame(instruments_info)

# for item in instruments_info[0:3]:
#     print(item)

instruments_info = pd.DataFrame.from_dict(instruments_info)

print(instruments_info)

# save so we don't need to send request every time

instruments_info.to_pickle("fx_bot/instrument_info/instruments.pkl")
