import os
import pandas as pd

# Función para cargar los datos de CoinMetrics
def load_coinmetrics_data():
    coinmetrics_data_path = 'data_coinmetrics'
    
    # Lista para almacenar los datos
    all_coinmetrics_data = []
    
    # Recorrer subcarpetas (BTC, ETH, USDT)
    for root, dirs, files in os.walk(coinmetrics_data_path):
        for file in files:
            if file.endswith('.csv'):
                # Cargar el archivo CSV
                file_path = os.path.join(root, file)
                print(f"Cargando archivo CoinMetrics: {file_path}")  # Debug: Verificar qué archivos se están cargando
                df = pd.read_csv(file_path)
                
                # Añadir la columna de asset (cripto) en minúsculas
                asset = root.split(os.sep)[-1].lower()
                df['asset'] = asset
                
                # Agregar el DataFrame a la lista
                all_coinmetrics_data.append(df)
    
    # Verificar si hay datos antes de concatenar
    if all_coinmetrics_data:
        combined_coinmetrics_df = pd.concat(all_coinmetrics_data, ignore_index=True)
        return combined_coinmetrics_df
    else:
        print("No se encontraron archivos CSV en la carpeta de CoinMetrics.")
        return None

# Función para cargar los datos de Binance
def load_binance_data():
    binance_data_path = 'data_binance/market_trades'
    
    all_binance_data = []
    
    for root, dirs, files in os.walk(binance_data_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Cargando archivo Binance: {file_path}")  # Debug para archivos de Binance
                
                # Intentar cargar el CSV
                df = pd.read_csv(file_path)
                
                # Extraer la moneda fiat y cripto de la estructura de carpetas y convertir a minúsculas
                fiat_currency = root.split(os.sep)[-2].lower()  # ARS
                crypto_currency = root.split(os.sep)[-1].lower()  # BTC, ETH
                
                # Añadir las columnas de fiat_currency y crypto_currency
                df['fiat_currency'] = fiat_currency
                df['crypto_currency'] = crypto_currency
                
                all_binance_data.append(df)
    
    if all_binance_data:
        combined_binance_df = pd.concat(all_binance_data, ignore_index=True)
        return combined_binance_df
    else:
        print("No se encontraron archivos CSV en la carpeta de Binance.")
        return None

# Función para calcular el volumen en USD
def calculate_usd_volume():
    # Cargar datos de Binance
    binance_data = load_binance_data()
    
    # Verificar si se cargaron los datos de Binance
    if binance_data is not None:
        # Convertir el timestamp de Binance a datetime
        binance_data['timestamp'] = pd.to_datetime(binance_data['timestamp']).dt.tz_localize(None)
    else:
        print("No se cargaron datos de Binance.")
        return
    
    # Cargar datos de CoinMetrics
    coinmetrics_data = load_coinmetrics_data()
    
    if coinmetrics_data is not None:
        # Convertir el timestamp de CoinMetrics a datetime
        coinmetrics_data['time'] = pd.to_datetime(coinmetrics_data['time']).dt.tz_localize(None)
        
        # Filtrar las criptomonedas con precios disponibles
        binance_data = binance_data[binance_data['crypto_currency'].isin(coinmetrics_data['asset'].unique())]
        
        # Combinar datos de Binance con los precios de CoinMetrics
        merged_df = pd.merge(
            binance_data, 
            coinmetrics_data, 
            left_on=['timestamp', 'crypto_currency'], 
            right_on=['time', 'asset'], 
            how='inner'
        )
        
        # Crear columna 'volumeUSD' multiplicando el volumen por el precio en USD
        merged_df['volumeUSD'] = merged_df['volume'] * merged_df['PriceUSD']
        
        # Guardar los resultados
        output_path = 'data_processed/volume_usd.csv'
        merged_df.to_csv(output_path, index=False)
        
        print(f"Archivo generado correctamente: {output_path}")
    else:
        print("No se pudo calcular el volumen en USD porque no hay datos de CoinMetrics disponibles.")

# Ejecutar la función
calculate_usd_volume()
