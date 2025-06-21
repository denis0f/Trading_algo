import threading
import time
from pprint import pprint
import os 
import json
import logging
import websocket
import numpy as np
import talib as tl
from logging.handlers import RotatingFileHandler
#this is from the binance-connect 

from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient

#setting the logger 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s <-> %(levelname)s -> %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logs_dir = "logs"

    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, "bot_logs.log"),
        maxBytes=1048576 * 5,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s <-> %(levelname)s -> %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


#binance basic urls and api
BINANCE_TESTNET_BASE_URL = "wss://testnet.binance.vision/ws"
BINANCE_BASE_URL = "wss://stream.binance.com:9443"
symbol = "ethusdt"
STREAM_NAME = f"{symbol}@kline_1m"
LIVE_FULL_WS_URL = f"{BINANCE_BASE_URL}/ws/{STREAM_NAME}"
TESTNET_FULL_WS_URL = f"{BINANCE_TESTNET_BASE_URL}/ws/{STREAM_NAME}"
#initialize the empty list to track the close prices as they are received
closes = []
#rsi info 
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
is_in_position = False


stop_event = threading.Event()

def on_open(ws):
    logger.info("The websocket is now open.")

def on_close(ws, close_status_code, close_msg):
    logger.info(f"Websocket was closed. Code: {close_status_code} & Message: {close_msg}")



def on_error(ws, error):
    logger.error(f"Websocket error: {error}", exc_info=True)

def on_message(ws, message):
    try:
        global closes
        ws_data = json.loads(message)
        
        kline_data = ws_data["k"]
        pprint(kline_data)

        is_kline_closed = kline_data["x"]
        

        if is_kline_closed:
            close_price = kline_data["c"]
            closes.append(close_price)
            print(closes)

            if len(closes) > RSI_PERIOD:
                closes_nparray = np.array(closes)
                rsi = tl.RSI(closes_nparray, timeperiod=RSI_PERIOD)
                current_rsi = rsi[-1]
                if current_rsi > RSI_OVERBOUGHT:
                    if is_in_position:
                        logger.info("Overbought but....You are already in a trade,,, nothing to do now!!!! !!!")
                    else:
                        logger.info("OverBought!!! Sell! Sell! Sell!")
                        #binance sell order execution here 
                elif current_rsi < RSI_OVERSOLD:
                    if is_in_position: 
                        logger.info("Oversold but....You are already in a trade,,, nothing to do now!!!! !!!")

                    else:
                        logger.info("OverSold!!! Buy! Buy! Buy!")
                        #binance buy order



    except json.JSONDecodeError as e:
        logger.error(f"Failed to convert the data recieved to Python Dict structure: {e}")
    except Exception as e:
        logger.error(f"Error processing the message recieved: {e}")





if __name__ == "__main__":
   
    

    # try:
    live_ws = websocket.WebSocketApp(LIVE_FULL_WS_URL, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
    live_ws.run_forever()
    #     testnet_api = websocket.WebSocketApp()
    #     ws_thread = threading.Thread(target=live_ws.run_forever, kwargs={"dispatcher": "auto_install"})
    #     ws_thread.daemon = True
    #     ws_thread.start()
        
    # except KeyboardInterrupt:
    #     logger.info("Keyboard interuprution. Signaling threads to stop...")
    # finally:
    #     logger.info("Attempting the shutdown of the websocket correct shutdown...")
    #     live_ws.close()
    #     ws_thread.join()
    #     logger.info("Program exited cleanly")


