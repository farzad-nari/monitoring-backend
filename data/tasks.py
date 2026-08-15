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
    config = load_config()
    window_size = config.get('window_size', 288)

    dataframe = read_csv_files()

    new_records = 0
    if not dataframe.empty:
        save_raw_data(dataframe)
        new_records = len(dataframe)
        dataframe = clean_data(dataframe)
        dataframe = add_features(dataframe)
        save_processed_data(dataframe)
        cache_realtime_data(dataframe)

    job_records = 0
    total = ProcessedData.objects.count()
    if total >= window_size:
        job = ProcessingJob.objects.create(status='processing', window_size=window_size)
        records = ProcessedData.objects.order_by('-timestamp')[:window_size]
        job.processed_data.set(records)
        job_records = job.processed_data.count()

    return f"new records: {new_records}, job records: {job_records}"