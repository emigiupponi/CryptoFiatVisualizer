import pandas as pd
import plotly.graph_objects as go
import time
import os

# Cargar el archivo CSV
file_path = 'data/processed/03_merge_usdvol.csv'
data = pd.read_csv(file_path)
print("Archivo cargado correctamente")

# Verifica que los nombres de columna sean correctos
print("Columnas en la base de datos:", data.columns)

# Filtrar los datos para pares en ARS (Argentina)
start_time = time.time()
data_argentina = data[data['quote_asset'] == 'ARS'].copy()  # Filtrado para pares en ARS
print(f"Filtrado de ARS completado en {time.time() - start_time} segundos")

# Convertir 'timestamp' a formato de fecha
start_time = time.time()
data_argentina['timestamp'] = pd.to_datetime(data_argentina['timestamp'], errors='coerce')
print(f"Conversión de fechas completada en {time.time() - start_time} segundos")

# Agrupar por 'timestamp' para obtener el volumen diario en USD
start_time = time.time()
data_daily_volume = data_argentina.dropna(subset=['timestamp']).groupby('timestamp').agg({'volume_usd_base': 'sum'}).reset_index()
print(f"Agrupamiento completado en {time.time() - start_time} segundos")

# Verifica que data_daily_volume esté correctamente creado
print(data_daily_volume.head())

# Crear el gráfico de líneas
start_time = time.time()
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data_daily_volume['timestamp'],
    y=data_daily_volume['volume_usd_base'],
    mode='lines',
    line=dict(color='darkblue', width=2),
    name='Daily Volume in USD'
))
print(f"Creación del gráfico completada en {time.time() - start_time} segundos")

# Guardar el gráfico en HTML en la carpeta de salida
output_dir = 'output/plots/color'
os.makedirs(output_dir, exist_ok=True)  # Asegura que la carpeta exista
output_path = os.path.join(output_dir, "daily_volume_ars_usd.html")

start_time = time.time()
fig.write_html(output_path)
print(f"Guardado del gráfico completado en {time.time() - start_time} segundos")

# Mostrar el gráfico en pantalla
fig.show()
