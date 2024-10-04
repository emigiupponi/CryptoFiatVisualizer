import sys
import os

# Agregar la ruta del módulo "modules" al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

# Ahora puedes importar los métodos del archivo data_loader.py
from data_loader import obtener_info_pares_binance, obtener_datos_y_guardar_csv

def test_obtener_info_pares_binance():
    pares = obtener_info_pares_binance()
    print(f"Total de pares obtenidos: {len(pares)}")
    print(pares)

def test_obtener_datos_y_guardar_csv():
    # Un ejemplo de cómo podrías probar la descarga de datos para un par específico.
    # Asegúrate de que el par exista en Binance, aquí usamos BTCUSDT como ejemplo.
    obtener_datos_y_guardar_csv('BTCUSDT', 'BTC', 'USDT')

if __name__ == "__main__":
    print("Probando obtener_info_pares_binance()")
    test_obtener_info_pares_binance()

    print("\nProbando obtener_datos_y_guardar_csv()")
    test_obtener_datos_y_guardar_csv()
