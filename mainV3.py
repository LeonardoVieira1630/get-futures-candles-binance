import os
import ccxt
import pandas as pd
import time

# Configurar a exchange Binance Futures
exchange = ccxt.binance({
    'rateLimit': 1000,  # Limite de taxa de chamadas por minuto
    'enableRateLimit': True,  # Habilitar o limite de taxa
    'urls': {
        'api': {
            'public': 'https://fapi.binance.com/fapi/v1',
            'private': 'https://fapi.binance.com/fapi/v1',
        },
    },
})

# Símbolo do par de negociação e intervalo de tempo (por exemplo, BTC/USDT e 1m)
symbol = 'BTCUSDT'
timeframe = '1m'

# Defina o tamanho do batch (lote) de dados
batch_size = 100000

# Nome do arquivo CSV onde os dados serão salvos
csv_file = 'binance_futures_1m_candles.csv'

# Verifique a data e hora atual
current_time = int(time.time() * 1000)  # Tempo atual em milissegundos

# Inicializar uma lista vazia para armazenar os dados
ohlcvs_all = []

while True:
    # Obter dados de candlesticks em batch
    ohlcvs = exchange.fetch_ohlcv(symbol, timeframe, limit=1000, params={'endTime': current_time})
    if len(ohlcvs) == 0:
        break

    # print(ohlcvs)
    # print(" ")

    ohlcvs.reverse()

    # Adicionar os dados ao final da lista
    ohlcvs_all.extend(ohlcvs)

    # Atualizar o tempo de início para a próxima solicitação
    #current_time = current_time - 60000 * 1500  # Adicione 60 segundos (1 minuto) ao último timestamp
    previous_end_time = ohlcvs[-1][0]   

    current_time = previous_end_time 
    # Respeitar o rateLimit
    time.sleep(exchange.rateLimit / 1000)  # Convertemos para segundos

    # Se acumulou dados suficientes para um batch, salve no mesmo arquivo CSV
    if len(ohlcvs_all) >= batch_size:
        # Criar um DataFrame com os dados do candlesticks
        df = pd.DataFrame(ohlcvs_all, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Converter a coluna de timestamp para um formato de data e hora legível
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Salvar os dados no arquivo CSV
        df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
        ohlcvs_all = []
        
    


print(f'Dados do candlesticks de 1 minuto salvos continuamente em "{csv_file}"')
