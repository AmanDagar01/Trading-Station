# This file contain all broker related functions.
# like:
# 1. connection with broker.
# 2. account info, current open positions, buy function, sell function, modify order.
# 3. Get ticker data(live, historical).


from binance.client import Client
from binance.enums import *
import keys
import broker
import pandas as pd

# Replace with your API keys from Binance
API_KEY = keys.api
API_SECRET = keys.secret

# Initialize the client for futures trading
client = Client(API_KEY, API_SECRET)

# to execute trade 
def execute_trade(side, quantity):
    """Execute a trade order."""
    try:
        order = broker.client.futures_create_order(
            symbol=keys.SYMBOL,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"Order executed: {side} {quantity} {keys.SYMBOL}")
        return order
    except Exception as e:
        print(f"Error executing trade: {e}")
        return None


# to get latest data
def get_latest_data():
    """Fetch the latest kline data from Binance."""
    klines = broker.client.futures_klines(symbol=keys.SYMBOL, interval=KLINE_INTERVAL_1MINUTE, limit=keys.LONG_MA)
    data = {
        'timestamp': [int(k[0]) for k in klines],
        'open': [float(k[1]) for k in klines],
        'high': [float(k[2]) for k in klines],
        'low': [float(k[3]) for k in klines],
        'close': [float(k[4]) for k in klines],
        'volume': [float(k[5]) for k in klines],
    }
    return pd.DataFrame(data)














'''
# Get account balance and other details
#account_info = client.futures_account()
#print(account_info)


# Get open positions
positions = client.futures_position_information()
for position in positions:
    print(position)


# Place a market buy order
buy_order = client.futures_create_order(
    symbol='ETHUSDT',
    side='BUY',
    type='MARKET',
    quantity=0.01  # Adjust quantity as needed
)
print(buy_order)

# Place a market sell order
sell_order = client.futures_create_order(
    symbol='ETHUSDT',
    side='SELL',
    type='MARKET',
    quantity=0.01  # Adjust quantity as needed
)
print(sell_order)


# Cancel an order
cancel_response = client.futures_cancel_order(
    symbol='ETHUSDT',
    orderId='your_order_id'
)
print(cancel_response)

# Modify by creating a new order
modified_order = client.futures_create_order(
    symbol='ETHUSDT',
    side='BUY',
    type='LIMIT',
    price=1700.00,  # Example price
    quantity=0.01,
    timeInForce='GTC'
)
print(modified_order)




# Fetch the latest price of a symbol
ticker = client.futures_symbol_ticker(symbol='ETHUSDT')
print(ticker)


# Fetch historical Kline/candlestick data
from binance.enums import *

# Example: Get 1-minute candlestick data
candles = client.futures_klines(
    symbol='ETHUSDT',
    interval=KLINE_INTERVAL_1MINUTE,
    limit=10  # Fetch last 10 candles
)
for candle in candles:
    print(candle)





'''