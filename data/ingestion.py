import pandas as pd
import os
import shutil
import uuid


def read_csv_files(folder_path='datasets/incoming/', processed_path='datasets/processed/'):
    os.makedirs(processed_path, exist_ok=True)
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not files:
        return pd.DataFrame()

    all_data = []
    required_columns = ['timestamp', 'param1', 'param2', 'param3', 'param4', 'param5']

    for file in files:
        filepath = os.path.join(folder_path, file)
        df = pd.read_csv(filepath)

        if all(col in df.columns for col in required_columns):
            all_data.append(df)
            shutil.move(filepath, os.path.join(processed_path, file))

    if all_data:
        dataframe = pd.concat(all_data, ignore_index=True)
        dataframe['record_id'] = [str(uuid.uuid4()) for _ in range(len(dataframe))]
        return dataframe
        
    return pd.DataFrame()

    
