import requests
import pandas as pd
import os

# Lista completa de monedas fiat
fiat_currencies = [
    'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'INR', 'RUB', 
    'BRL', 'ARS', 'NGN', 'TRY', 'MXN', 'ZAR', 'PLN', 'SEK', 'NOK', 'DKK', 
    'HKD', 'SGD', 'NZD', 'KRW', 'THB', 'MYR', 'IDR', 'PHP', 'VND', 'CZK', 
    'HUF', 'RON', 'BGN', 'HRK', 'RSD', 'UAH', 'KZT', 'AZN', 'GEL', 'BYN',
    'EGP', 'ILS', 'SAR', 'AED', 'QAR', 'KWD', 'BHD', 'OMR', 'TND', 'MAD', 
    'DZD', 'TWD', 'LKR', 'PKR', 'BDT', 'KES', 'TZS', 'UGX', 'GHS', 'XAF', 
    'XOF', 'XPF', 'MUR', 'SCR', 'MGA', 'ZMW', 'MWK', 'BWP', 'NAD', 'SLL',
    'LRD', 'LSL', 'SZL', 'MZN', 'BIF', 'CDF', 'DJF', 'ETB', 'GNF', 'HTG',
    'LRD', 'MGA', 'NPR', 'PGK', 'PGK', 'SHP', 'SLL', 'SOS', 'SSP', 'STD',
    'SYP', 'TOP', 'TTD', 'TWD', 'VUV', 'WST', 'XCD', 'YER', 'ZMW'
]

# Definir la carpeta base donde se guardarán los archivos CSV
base_folder = 'datos_historicos_binance'

# Crear la carpeta base si no existe
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# Función para obtener la información de pares de Binance
def obtener_info_pares_binance():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        info_pares = {}
        for symbol_info in data['symbols']:
            symbol = symbol_info['symbol']
            base_currency = symbol_info['baseAsset']
            quote_currency = symbol_info['quoteAsset']
            info_pares[symbol] = {'base_currency': base_currency, 'quote_currency': quote_currency}
        return info_pares
    else:
        print(f"Error al obtener información sobre los pares de Binance. Código de estado: {response.status_code}")
        return None

# Función para guardar los datos en la estructura de carpetas
def guardar_datos_binance(symbol, base_currency, quote_currency, data):
    fiat_currency = base_currency if base_currency in fiat_currencies else quote_currency
    crypto_currency = base_currency if base_currency not in fiat_currencies else quote_currency
    
    fiat_folder_path = os.path.join(base_folder, fiat_currency)
    if not os.path.exists(fiat_folder_path):
        os.makedirs(fiat_folder_path)
    
    crypto_folder_path = os.path.join(fiat_folder_path, crypto_currency)
    if not os.path.exists(crypto_folder_path):
        os.makedirs(crypto_folder_path)
    
    for month, df_month in data.groupby(data['timestamp'].dt.to_period('M')):
        file_path = os.path.join(crypto_folder_path, f'{fiat_currency.lower()}_{crypto_currency.lower()}_{month.start_time.strftime("%Y-%m")}.csv')
        df_month.to_csv(file_path, index=False)

# Función para descargar y guardar datos de Binance
def obtener_datos_binance(symbol, base_currency, quote_currency):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'number_of_trades', 
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        guardar_datos_binance(symbol, base_currency, quote_currency, df)
    else:
        print(f"Error al descargar datos para {symbol}. Código de estado: {response.status_code}")

# Descargar y guardar los datos de todos los pares de interés
info_pares = obtener_info_pares_binance()
if info_pares:
    for symbol, details in info_pares.items():
        base_currency = details['base_currency']
        quote_currency = details['quote_currency']
        if base_currency in fiat_currencies or quote_currency in fiat_currencies:
            obtener_datos_binance(symbol, base_currency, quote_currency)
