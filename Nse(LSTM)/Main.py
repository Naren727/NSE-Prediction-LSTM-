import warnings
import pandas as pd
import numpy as np
from datetime import date

# API to get nse stock data given a time interval;Mostly Historical data
from nsepy import get_history

# API to remotely execute ipynb files from python script
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# API to get real time data
from nsepython import *

# Technical Analysis Library
import ta as ta
from pandas.io.json import json_normalize
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volume import VolumeWeightedAveragePrice

# Suppressing Some warnings
pd.options.mode.chained_assignment = None  # default='warn'
warnings.filterwarnings("ignore")
status = "Closed"


# Function to format the data, perform an initial rough feature selection and add indicators that may be useful
def format_HistoricalData(dat, ohlc):
    df = pd.DataFrame(dat)
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    new_df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Date']]
    new_df = new_df.append(ohlc, ignore_index=True)

    # Converting datatypes to float
    # new_df = pd.to_numeric(new_df)
    new_df['Open'] = new_df.Open.astype(float)
    new_df['High'] = new_df.High.astype(float)
    new_df['Low'] = new_df.Low.astype(float)
    new_df['Close'] = new_df.Close.astype(float)

    vwap = ta.volume.VolumeWeightedAveragePrice(new_df["High"], new_df["Low"], new_df["Close"], new_df["Volume"],
                                                window=14)
    rsi = ta.momentum.RSIIndicator(new_df['Close'], window=14, fillna=True)
    ema = ta.trend.EMAIndicator(new_df['Close'], window=14, fillna=True)
    md = ta.trend.MACD(new_df['Close'], window_slow=28, window_fast=14, fillna=True)

    # Setting Indicators
    new_df["VWAP"] = vwap.volume_weighted_average_price()
    new_df["RSI"] = rsi.rsi()
    new_df["MACD"] = md.macd()
    new_df["EMA"] = ema.ema_indicator()

    # Setting Target or Y value which gives the next day's closing price
    new_df["Target"] = new_df['Close'].shift(-1)
    # Target class shows the sentiment : BULLISH(1) or BEARISH(0)
    new_df['TargetClass'] = [1 if new_df.Target[i] > new_df.Close[i] else 0 for i in range(len(new_df))]

    predictor_input = new_df.tail(1)

    # If the market is open then we predict to the open price of the stock
    if status == 'Open':
        predictor_input["Target"] = predictor_input["Open"]
        new_df = new_df.append(predictor_input)
    # to store the last row for later prediction :

    new_df = new_df.dropna()

    return new_df


# Function to use the api and fetch the data from the server
def Fetch_User_Data(user_input, ohlc):
    try:
        data = get_history(symbol=user_input, start=date(2003, 1, 1), end=date.today())
        df = format_HistoricalData(data, ohlc)
        df.to_csv('Training_data.csv')
    except ConnectionError:
        print("Connection Error from nsepython API.High chance of market close")
    except AttributeError:
        print("Attribute Error Occurred")
    except TimeoutError:
        print("Connection Timeout")
    except:
        print("Unknown Error occurred.test nsepy api?")


def Fetch_Predictions():
    with open("Nse_Model.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb)
    with open('Nse_Model.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    predictions = pd.read_csv("Prediction.csv")
    return predictions


def Plot():
    plot = 1
    # Plot the graph here


def Get_RT_Data(symbol, pos, attribute="lastPrice"):
    res = np.where(pos["symbol"] == symbol, pos[attribute], np.nan)
    return res


def Fetch_ohlc(inp):
    try:
        global status
        positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
        stat = json_normalize(positions['marketStatus'])
        status = stat['marketStatus'].values
        positions = json_normalize(positions['data'])

        Nifty50 = list(positions["symbol"])
        if inp in Nifty50:
            ohlc = pd.DataFrame()

            ohlc["Open"] = Get_RT_Data(inp, positions, "open")
            ohlc["High"] = Get_RT_Data(inp, positions, "dayHigh")
            ohlc["Low"] = Get_RT_Data(inp, positions, "dayLow")
            ohlc["Close"] = Get_RT_Data(inp, positions, "previousClose")
            ohlc["Volume"] = Get_RT_Data(inp, positions, "totalTradedVolume")

            ohlc["Date"] = date.today()
            ohlc.set_index("Date")
            ohlc = ohlc.dropna()
            return ohlc
        else:
            print("Please enter a Nifty 50 Stock and try again")

    except ConnectionError:
        print("Connection Error from nsepython API.High chance of market close")
    except AttributeError:
        print("Attribute Error Occurred")
    except TimeoutError:
        print("Connection Timeout")
    except:
        print("Unknown Error occured.test nsepython api?")


# Main Method :
if __name__ == "__main__":
    inp = "CIPLA"
    ohlc = Fetch_ohlc(inp)
    Fetch_User_Data(inp, ohlc)
    pred_df = Fetch_Predictions()
    print("Prediction for the Stock Price : ",pred_df["Date"].tail(1).values," ",pred_df["Target"].tail(1).values)


# Enable GPU for tensorflows
# drop df.tail(1) in the ipynb and save it for testing :>
# add date column to both new_df & ohlc . file.csv must have a date column for plotting purposes :/
'''
   
    try:
        except ConnectionError:
        print("Connection Error from nsepy API")
    except AttributeError:
        print("Result Attribute not obtained from server")
    except:
'''
