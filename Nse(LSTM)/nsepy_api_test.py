from datetime import date
import pandas as pd

from nsepy import get_history

data = get_history(symbol="CIPLA", start=date(2023, 1, 1), end=date.today())
df = pd.DataFrame(data)
print(df.columns)
#df.to_csv("test.csv")

df.reset_index(inplace=True)
df.rename(columns = {'index':'Date'}, inplace = True)