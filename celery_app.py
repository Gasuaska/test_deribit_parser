import os

from celery import Celery

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

celery_app = Celery(
    'price_worker',
    broker=broker_url,
    backend=broker_url,
    include=['tasks']
)

celery_app.conf.beat_schedule = {
    'fetch-prices-every-minute': {
        'task': 'tasks.fetch_prices',
        'schedule': 60.0
    }
}

celery_app.conf.timezone = 'UTC'
