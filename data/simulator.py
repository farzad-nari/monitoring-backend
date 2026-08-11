import os
from datetime import datetime, timedelta
import random
import pandas as pd

def generate_simulated_data(num_records=100, output_dir='datasets/incoming/'):
    os.makedirs(output_dir, exist_ok=True)
    data = []
    start_time = datetime.now() - timedelta(minutes=num_records)

    for i in range(num_records):
        timestamp = start_time + timedelta(minutes=i)
        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S') + '+00:00',
            'param1': random.uniform(100, 300),
            'param2': random.uniform(40, 80),
            'param3': random.uniform(1000, 2000),
            'param4': random.uniform(-50, 50),
            'param5': random.uniform(48, 52),
            'unit_id': f'unit-{random.randint(1, 5)}',
            'equipment_status': random.choice(['normal', 'warning', 'error'])
        })

    df = pd.DataFrame(data)
    filename = f"simulated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    return filepath
