from celery import shared_task
from data.ingestion import read_csv_files
from data.storage import save_raw_data, save_processed_data
from data.preprocessing import clean_data
from data.feature_engineering import add_features
from core.cache import cache_realtime_data
from core.config_loader import load_config
from .models import ProcessedData, ProcessingJob


@shared_task
def process_new_data():
    dataframe = read_csv_files()
    if dataframe.empty:
        return "no new data"

    save_raw_data(dataframe)
    dataframe = clean_data(dataframe)
    dataframe = add_features(dataframe)
    save_processed_data(dataframe)
    cache_realtime_data(dataframe)

    config = load_config()
    window_size = config.get('window_size', 288)

    total = ProcessedData.objects.count()

    if total >= window_size:
        job = ProcessingJob.objects.create(status='processing', window_size=window_size)
        records = ProcessedData.objects.order_by('-timestamp')[:window_size]
        job.processed_data.set(records)
    return f'processed {len(dataframe)} records'



    