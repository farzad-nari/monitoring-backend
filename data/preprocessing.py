from core.config_loader import load_config
import pandas as pd

def clean_data(dataframe):
    if dataframe.empty:
        return dataframe

    config = load_config()

    required_columns = ['timestamp', 'param1', 'param2', 'param3', 'param4', 'param5']
    df = dataframe.dropna(subset=required_columns)

    for param, limits in config['parameters'].items():
        if param in df.columns:
            df = df[(df[param] >= limits['min']) & (df[param] <= limits['max'])]

    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df['timestamp'] = df['timestamp'].dt.floor('1min')
    df = df.set_index('timestamp')

    numeric_columns = ['param1', 'param2', 'param3', 'param4', 'param5']
    df[numeric_columns] = df[numeric_columns].resample('1min').interpolate('linear')

    df = df.reset_index()

    return df


