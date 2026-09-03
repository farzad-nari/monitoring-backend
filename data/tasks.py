from celery import shared_task
from data.ingestion import read_csv_files
from data.storage import save_raw_data, save_processed_data
from data.preprocessing import clean_data
from data.feature_engineering import add_features
from core.cache import cache_realtime_data
from core.config_loader import load_config
from .models import ProcessedData, ProcessingJob
from datetime import datetime, timezone
from analysis.models import AnalysisResult
import requests


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
        job = ProcessingJob.objects.create(status='pending', window_size=window_size)
        records = ProcessedData.objects.order_by('-timestamp')[:window_size]
        job.processed_data.set(records)
        job_records = job.processed_data.count()

        send_job_to_ml_engine.delay(job.id)

    return f"new records: {new_records}, job records: {job_records}"


@shared_task
def send_job_to_ml_engine(job_id):
    job = ProcessingJob.objects.get(id=job_id)
    job.status = 'processing'
    job.save()

    records = [
        {
            **record,
            'timestamp': record['timestamp'].isoformat().replace('+00:00', 'Z')
        }
        for record in job.processed_data.values(
            'timestamp',
            'param1',
            'param2',
            'param3',
            'param4',
            'param5'
        )
    ]

    payload = {
        'request_id': str(job.request_id),
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'window_size': job.window_size,
        'records': records
    }

    config = load_config()
    ml_engine_url = config.get('ml_engine_url')

    try:
        response = requests.post(
            f'{ml_engine_url}/api/predict',
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        processed_at = datetime.fromisoformat(data['processed_at'].replace('Z', '+00:00'))

        AnalysisResult.objects.create(
            job = job,
            request_id = data['request_id'],
            processed_at = processed_at,
            forecast = data['forecast'],
            risk_score = data['risk_score'],
            risk_level = data['risk_level'],
            risk_breakdown = data['risk_breakdown'],
            anomalies = data['anomalies'],
            decisions = data['decisions'],
        )
        job.status = 'completed'
        job.completed_at = datetime.now(timezone.utc)

    except Exception:
        job.status = 'failed'
        raise

    finally:
        job.save()

    return {'status': 'success', 'job_id': job_id}

    