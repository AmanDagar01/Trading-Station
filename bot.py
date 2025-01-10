# this file contain the logic for the trade.
# For the tryl i am using the logic my pre build logic of rsi and ma.

# implement: api limit exceed problem.
# implement: it uses 45% of current capital (i think it would be benificial also no need to adjust capital again and again).
# ipmlement: more than one coin to find the suitable trade
  # implement: two ways one is one trade ata a time or two tarde at a time.
# implement: two modes one is live money and one is paper money.
# implemrnt: one text file that will store the info of trades or only the profit persent and all.
# try: how ml can affect the parameters values(weights) of indicaters to enhance the porfits.
# try: try to make one backtesting file also that will use the diff settings of indicaters and provide the backtesting result with a datas like 
#      profit percent, max drawdown, max profit, winning rate, win trade, loose trade, total number of trades.
#      and any other necessary parameters that are needed.

# make code clean and understable.
# try to keep only the logic scripts to this file rest all put in different file.
    # orders one in broker.
    # data one in data file.
    



import time
import pandas as pd
import numpy as np
import broker
import keys


#paper account (for testing)
paper_money  = 100
position = 0
percent_profit = 0
total_trade = 0



def calculate_indicators(df):
    """Calculate MA and RSI for real-time trading."""
    df['short_ma'] = df['close'].rolling(window=keys.SHORT_MA).mean()
    df['long_ma'] = df['close'].rolling(window=keys.LONG_MA).mean()
    
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=keys.RSI_PERIOD).mean()
    avg_loss = pd.Series(loss).rolling(window=keys.RSI_PERIOD).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df





def live_trading():
    """Main live trading loop."""
    position = None
    entry_price = 0
    exit_price = 0
    global total_trade,percent_profit,paper_money
    
    while True:
        # Get the latest data and calculate indicators
        df = broker.get_latest_data()
        df = calculate_indicators(df)
        latest_row = df.iloc[-1]
        
        if not pd.isna(latest_row['short_ma']) and not pd.isna(latest_row['long_ma']) and not pd.isna(latest_row['rsi']):
            if not position:
                if latest_row['short_ma'] > latest_row['long_ma'] and latest_row['rsi'] > keys.RSI_OVERSOLD:
                    # Open long position
                    #execute_trade(SIDE_BUY, QUANTITY)
                    entry_price = latest_row['close']
                    position = 100/entry_price
                    total_trade = total_trade +1
                    print(f'long at {entry_price}')
                    
                    position = "long"
                elif latest_row['short_ma'] < latest_row['long_ma'] and latest_row['rsi'] < keys.RSI_OVERBOUGHT:
                    # Open short position
                    #execute_trade(SIDE_SELL, QUANTITY)
                    entry_price = latest_row['close']
                    print(f'short at {entry_price}')
                    position = 100/entry_price
                    total_trade = total_trade +1
                    position = "short"
            else:
                if position == "long" and (latest_row['short_ma'] < latest_row['long_ma'] or latest_row['rsi'] > keys.RSI_OVERBOUGHT):
                    # Close long position
                    exit_price = latest_row['close']
                    #execute_trade(SIDE_SELL, QUANTITY)
                    print(f'close long at {exit_price}')
                    percent_profit = percent_profit + ((exit_price - entry_price)/entry_price)*1500
                    print(f'total profit percent is {percent_profit}% with a total trade of {total_trade}')
                    position = None
                elif position == "short" and (latest_row['short_ma'] > latest_row['long_ma'] or latest_row['rsi'] < keys.RSI_OVERSOLD):
                    # Close short position
                    #execute_trade(SIDE_BUY, QUANTITY)
                    exit_price = latest_row['close']
                    print(f'close short at {exit_price}')
                    percent_profit = percent_profit - ((exit_price - entry_price)/entry_price)*1500
                    print(f'total profit percent is {percent_profit}% with a total trade of {total_trade}')
                    position = None
        
        # Wait for the next iteration
        time.sleep(60)

# Run the live trading
if __name__ == "__main__":
    live_trading()
