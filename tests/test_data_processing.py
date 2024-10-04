# tests/test_data_processing.py

import sys
import os
import pandas as pd

# Añadir la carpeta principal al path para encontrar 'modules'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.data_processor import procesar_datos

if __name__ == "__main__":
    # Crear un DataFrame de prueba
    data = {
        'OpenTime': [1622548800000, 1622635200000],  # Timestamps en ms
        'CloseTime': [1622635200000, 1622721600000],  # Timestamps en ms
        'Volume': [100, 200],
        'Ignore': ['test', 'test']
    }

    df = pd.DataFrame(data)

    # Aplicar el procesamiento
    df_procesado = procesar_datos(df)
    
    print("DataFrame procesado:")
    print(df_procesado)
