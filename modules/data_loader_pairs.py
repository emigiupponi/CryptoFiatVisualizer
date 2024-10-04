import requests
import pandas as pd
import os

# Define the base folder where data will be stored
base_folder = 'data_binance'

# Create subfolders if they don't exist
market_trades_folder = os.path.join(base_folder, 'market_trades')
pair_info_folder = os.path.join(base_folder, 'pair_information')

for folder in [market_trades_folder, pair_info_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to retrieve information about all pairs from Binance
def get_binance_pairs_info():
    # URL for the Binance exchangeInfo endpoint
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    
    # Send a GET request to the endpoint
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response data to JSON format
        data = response.json()
        
        # Create a list to store the information about currency pairs
        pairs = []
        
        # Iterate over the data to extract relevant information for each pair
        for symbol_info in data['symbols']:
            symbol = symbol_info['symbol']
            base_currency = symbol_info['baseAsset']
            quote_currency = symbol_info['quoteAsset']
            
            # Store the information in the list
            pairs.append({'symbol': symbol, 'base_currency': base_currency, 'quote_currency': quote_currency})
        
        # Convert the list to a pandas DataFrame
        df_pairs = pd.DataFrame(pairs)
        return df_pairs
    else:
        print(f"Error retrieving Binance pairs information. Status code: {response.status_code}")
        return None

# Retrieve information about all Binance pairs
df_pairs = get_binance_pairs_info()

# Check if the information was successfully retrieved
if df_pairs is not None:
    # Save the DataFrame to a CSV file in the pair_information folder
    csv_file = os.path.join(pair_info_folder, 'binance_all_pairs.csv')
    df_pairs.to_csv(csv_file, index=False)
    print(f"File saved: {csv_file}")
else:
    print("Failed to retrieve Binance pairs information.")
