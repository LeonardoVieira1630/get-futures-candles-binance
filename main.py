import ccxt
import pandas as pd
import time

# Configurar a exchange Binance Futures
exchange = ccxt.binance({
    'rateLimit': 1200,  # Limite de taxa de chamadas por minuto
    'enableRateLimit': True,  # Habilitar o limite de taxa
})

# Símbolo do par de negociação e intervalo de tempo (por exemplo, BTC/USDT e 1m)
symbol = 'BTC/USDT'
timeframe = '1m'

# Inicializar uma lista vazia para armazenar os dados
ohlcvs_all = []

# Começar a partir do tempo atual e retroceder no tempo
end_time = int(time.time() * 1000)  # Tempo atual em milissegundos
limit = 1000  # Número de candlesticks por solicitação
previous_end_time = None

while True:
    if previous_end_time is not None and end_time >= previous_end_time:
        break

    # Obter dados de candlesticks
    ohlcvs = exchange.fetch_ohlcv(symbol, timeframe, limit=limit, params={'endTime': end_time})
    if len(ohlcvs) == 0:
        break

    # Adicionar os dados ao final da lista
    ohlcvs_all.extend(ohlcvs)

    # Atualizar o tempo de término para a próxima solicitação
    previous_end_time = ohlcvs[-1][0]
    end_time = previous_end_time - 1

    # Respeitar o rateLimit
    time.sleep(exchange.rateLimit / 1000)  # Convertemos para segundos

# Criar um DataFrame com os dados do candlesticks
df = pd.DataFrame(ohlcvs_all, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Converter a coluna de timestamp para um formato de data e hora
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Salvar os dados em um arquivo CSV
df.to_csv('binance_futures_1m_candles.csv', index=False)

print(f'Todos os dados de candlesticks de 1 minuto salvos em "binance_futures_1m_candles.csv"')
