from data.models import RawData, ProcessedData


def save_raw_data(dataframe):
    if dataframe.empty:
        return

    records = []
    for _, row in dataframe.iterrows():
        records.append(RawData(
            timestamp=row['timestamp'],
            param1=row['param1'],
            param2=row['param2'],
            param3=row['param3'],
            param4=row['param4'],
            param5=row['param5'],
            unit_id=row.get('unit_id'),
            equipment_status=row.get('equipment_status'),
            record_id=row.get('record_id')
        ))

    RawData.objects.bulk_create(records)


def save_processed_data(dataframe):
    if dataframe.empty:
        return

    records = []
    for _, row in dataframe.iterrows():
        raw_data = RawData.objects.filter(record_id=row.get('record_id')).first() if row.get('record_id') else None
        records.append(ProcessedData(
            raw_data=raw_data,
            record_id=row.get('record_id'), 
            timestamp=row['timestamp'],
            param1=row['param1'],
            param2=row['param2'],
            param3=row['param3'],
            param4=row['param4'],
            param5=row['param5'],
            unit_id=row.get('unit_id'),
            equipment_status=row.get('equipment_status'),
            param1_ma5m=row.get('param1_ma5m'),
            param1_ma15m=row.get('param1_ma15m'),
            param1_ma30m=row.get('param1_ma30m'),
            param1_change_rate=row.get('param1_change_rate'),
            param2_change_rate=row.get('param2_change_rate'),
            hour_of_day=row.get('hour_of_day'),
            day_of_week=row.get('day_of_week'),
            month=row.get('month'),
            param1_deviation_7d=row.get('param1_deviation_7d')
        ))

    ProcessedData.objects.bulk_create(records)
