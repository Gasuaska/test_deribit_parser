from celery import Celery

celery_app = Celery(
    'price_worker',
    broker = 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0',
    include=['tasks']
)

celery_app.conf.beat_schedule = {
    'fetch-prices-every-minute': {
        'task': 'tasks.fetch_prices',
        'schedule': 60.0
    }
}

celery_app.conf.timezone = 'UTC'
