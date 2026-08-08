from django.core.cache import cache


def cache_realtime_data(dataframe):
    if dataframe.empty:
        return

    last_row = dataframe.iloc[-1]
    for param in ['param1', 'param2', 'param3', 'param4', 'param5']:
        cache.set(f'realtime:{param}', last_row[param], timeout=60)


def get_realtime_data():
    data = {}
    for param in ['param1', 'param2', 'param3', 'param4', 'param5']:
        data[param] = cache.get(f'realtime:{param}')

    return data


