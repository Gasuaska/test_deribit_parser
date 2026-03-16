import time
import logging

from celery_app import celery_app

from app.utils import get_price_from_service
from app.database import SessionLocal, PriceDB
from app.constants import TICKERS
from app.exceptions import DeribitClientError

@celery_app.task
def fetch_prices():
    session = SessionLocal()
    tickers = TICKERS
    for ticker in tickers:
        try:
            price = get_price_from_service(ticker)
        except DeribitClientError as e:
            logging.error(f'Failed to fetch {ticker}: {e}')
            continue
        item = PriceDB(
            ticker=ticker,
            price=price,
            timestamp=int(time.time())
        )
        session.add(item)
    session.commit()
    logging.info(f'Price for {ticker} sucsessfully saved.')
    session.close()
    
