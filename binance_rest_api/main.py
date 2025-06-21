from dotenv import load_dotenv
import numpy as np
import talib
from binance.spot import Spot
import os 
import json
import pandas as pd

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

client = Spot(api_key=API_KEY, api_secret=API_SECRET_KEY, testnet=True)


#get all tickers 
def get_tickers()->pd.DataFrame:
    """
        the function returns the symbols and the limits of the infomation concerning the symbols
    """
    tickers = client.exchange_info()
    tickers = json.loads(tickers)
    df=pd.DataFrame(tickers)
    return df 



#get the account info 
def get_account_info():
    account_details = client.account()
    account_details = json.loads(account_details)
    return pd.DataFrame(account_details)

#get the active positions 
def get_active_positions()-> list:
    """the function returns a list of all open positions """
    positions = client.get_open_orders()

    return list(positions)

#placing a new order 
def place_order(symbol:str, quantity:float, type:str, side:str):
    """the function return the details of the order placed"""

    order_params = {
        "symbol": symbol,
        "type": type,
        "quantity": quantity, 
        "side": side
    }
    order = client.new_order(**order_params)
    return order

#technical trading logic generation
def technicals_trading_logic():
    """the function calculates the rsi and the moving averages and then returns the side of the buy to take
    in reference to the price """
    pass

#model generation of the sentiment and also some technical analysis
def model_predictions():
    """consists of a neural network model that takes in the news and also the prices and tries to predict the sentiment side of the anlysis"""
    pass

#execution main function 
def main():
    """this is the main fucntion where all the logic to take a trade executes after getting the sentiment and the techinical anlysis from the model_prediction 
    and the technical_trading_logic functions """
    pass




if __name__ == "__main__":
    pass