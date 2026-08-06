import pandas as pd


def add_features(dataframe):
    if dataframe.empty:
        return dataframe

    dataframe['param1_ma5m'] = dataframe['param1'].rolling(window=5).mean()
    dataframe['param1_ma15m'] = dataframe['param1'].rolling(window=15).mean()
    dataframe['param1_ma30m'] = dataframe['param1'].rolling(window=30).mean()

    dataframe['param1_change_rate'] = dataframe['param1'].pct_change()
    dataframe['param2_change_rate'] = dataframe['param2'].pct_change()

    dataframe['hour_of_day'] = dataframe['timestamp'].dt.hour
    dataframe['day_of_week'] = dataframe['timestamp'].dt.weekday
    dataframe['month'] = dataframe['timestamp'].dt.month

    dataframe['param1_deviation_7d'] = dataframe['param1'] - (
        (
        dataframe['param1'].shift(1 * 24 * 60) +
        dataframe['param1'].shift(2 * 24 * 60) +
        dataframe['param1'].shift(3 * 24 * 60) +
        dataframe['param1'].shift(4 * 24 * 60) +
        dataframe['param1'].shift(5 * 24 * 60) +
        dataframe['param1'].shift(6 * 24 * 60) +
        dataframe['param1'].shift(7 * 24 * 60)
        ) / 7
    )

    return dataframe
