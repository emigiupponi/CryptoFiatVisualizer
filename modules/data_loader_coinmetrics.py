from coinmetrics.api_client import CoinMetricsClient
import pandas as pd
import os

# Inicializar el cliente de CoinMetrics
client = CoinMetricsClient()

# Definir la carpeta base donde se guardarán los precios
base_folder = 'datos_precios_coinmetrics'

# Crear la carpeta base si no existe
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# Función para guardar los precios en la estructura de carpetas
def guardar_precios_coinmetrics(asset, data):
    asset_folder_path = os.path.join(base_folder, asset.upper())
    if not os.path.exists(asset_folder_path):
        os.makedirs(asset_folder_path)
    
    for month, df_month in data.groupby(data['time'].dt.to_period('M')):
        file_path = os.path.join(asset_folder_path, f'{asset.lower()}_{month.start_time.strftime("%Y-%m")}.csv')
        df_month.to_csv(file_path, index=False)

# Descargar precios históricos de CoinMetrics
def obtener_precios_coinmetrics():
    assets = ['btc', 'eth', 'usdt']
    metrics = ['PriceUSD']
    start_time = '2019-01-01'
    
    for asset in assets:
        price_data = client.get_asset_metrics(assets=[asset], metrics=metrics, frequency='1d', start_time=start_time)
        df_price = price_data.to_dataframe()
        df_price['time'] = pd.to_datetime(df_price['time'])
        guardar_precios_coinmetrics(asset, df_price)

# Ejecutar la descarga de precios
obtener_precios_coinmetrics()
