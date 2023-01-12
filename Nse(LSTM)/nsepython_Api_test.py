from nsepython import *
from pandas.io.json import json_normalize

positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
status = json_normalize(positions['marketStatus'])
# positions = json_normalize(positions['data'])
# print(positions.columns)
if status['marketStatus'].values == 'Closed':
    print("ok")
# new_df['TargetClass'] = [1 if new_df.Target[i] > new_df.Close[i] else 0 for i in range(len(new_df))]
