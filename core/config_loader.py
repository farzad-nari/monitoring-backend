import json
import os
from django.conf import settings

CONFIG_PATH = os.path.join(settings.BASE_DIR, 'data', 'config.json')

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)



