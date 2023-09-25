# 🕯️ Binance Futures Candlestick Data Collector 📈💹

This Python script collects candlestick data from Binance Futures for a specified trading pair and timeframe and saves it to a CSV file . It uses the CCXT library to interact with the Binance Futures API and can be configured using environment variables.

## Prerequisites 🧐

Before running this script, you need to set up a `.env` file to configure the trading pair and timeframe. Follow the steps below to create and configure the `.env` file:

1. Create a `.env` file in the same directory as the script.

2. Open the `.env` file using a text editor and add the following lines:

```.env
SYMBOL=ETHUSDT
TIMEFRAME=1m
```

Replace `ETHUSDT` with the trading pair you want to collect data for and `1m` with the desired timeframe.

## Installation 🛠️

1. Clone or download this repository to your local machine.

2. Navigate to the directory containing the script.

3. Install the required Python packages by running the following command:

```cmd
pip install -r requirements.txt
```

## Usage 🚀

To run the script, execute the following command in your terminal:

```python
python get_candles_futures_binance.py

```

The script will start collecting candlestick data for the specified trading pair and timeframe and save it to a CSV file named `futures_candles.csv`.

## Configuration ⚙️

You can modify the script's configuration by editing the `.env` file. Here are the available options:

- `SYMBOL`: The trading pair you want to collect data for (e.g., `ETHUSDT`, `BTCUSDT`, etc.).

- `TIMEFRAME`: The timeframe for candlestick data (e.g., `1m` for 1-minute intervals, `1h` for 1-hour intervals, etc.).
