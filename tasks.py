import time
import logging

from celery_app import celery_app

from utils import get_price_from_service
from database import SessionLocal, PriceDB
from constants import TICKERS
from exceptions import DeribitClientError

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
    
