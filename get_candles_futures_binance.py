import os
import ccxt
import pandas as pd
import time
from dotenv import load_dotenv


def get_candles():

    load_dotenv()
    symbol = os.getenv("SYMBOL")
    timeframe = os.getenv("TIMEFRAME")


    # Set up the Binance Futures exchange
    exchange = ccxt.binance({
        'rateLimit': 1000,  # Rate limit for API calls per minute
        'enableRateLimit': True,  # Enable rate limiting
        'urls': {
            'api': {
                'public': 'https://fapi.binance.com/fapi/v1',
                'private': 'https://fapi.binance.com/fapi/v1',
            },
        },
    })


    # Set the batch data size
    batch_size = 10000

    # CSV file name where the data will be saved
    csv_file = 'futures_candles.csv'

    # Check the current date and time
    current_time = int(time.time() * 1000)  # Current time in milliseconds

    # Initialize an empty list to store the data
    ohlcvs_all = []

    while True:
        # Get candlestick data in batch
        ohlcvs = exchange.fetch_ohlcv(symbol, timeframe, limit=1000, params={'endTime': current_time})
        if len(ohlcvs) == 0:
            break

 
        ohlcvs.reverse()

        # Add the data to the end of the list
        ohlcvs_all.extend(ohlcvs)

        # Update the start time for the next request
        previous_end_time = ohlcvs[-1][0]

        current_time = previous_end_time
        # Respect the rateLimit
        time.sleep(exchange.rateLimit / 1000)  # Convert to seconds

        # If enough data has accumulated for a batch, save it to the same CSV file
        if len(ohlcvs_all) >= batch_size:
            # Create a DataFrame with candlestick data
            df = pd.DataFrame(ohlcvs_all, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Convert the timestamp column to a readable date and time format
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Save the data to the CSV file
            df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
            ohlcvs_all = []

    print(f'Candlestick data for 1-minute intervals continuously saved in "{csv_file}"')



get_candles()