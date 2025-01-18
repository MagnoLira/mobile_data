import os
import pandas as pd
import csv

# It saves the data into csv with pandas 
def save_to_csv(filename, data, fieldnames=None):
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensures the existence of the directory
    if isinstance(data, list) and fieldnames:
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])  # Dataframe with only one line 
        if not os.path.exists(filename):
            df.to_csv(filename, index=False, mode='w', encoding='utf-8')
        else:
            df.to_csv(filename, index=False, mode='a', header=False, encoding='utf-8')
