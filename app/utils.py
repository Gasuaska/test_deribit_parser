import logging
import requests
from requests.exceptions import (HTTPError,
                                 ConnectionError,
                                 Timeout,
                                 RequestException)

from fastapi import HTTPException

from database import SessionLocal, PriceDB
from constants import DERIBIT_URL, TICKERS

def validate_ticker(ticker: str):
    ticker = ticker.lower()
    if ticker not in TICKERS:
        logging.error(f'Invalid ticker {ticker}')
        raise HTTPException(status_code=400, detail='Invalid ticker')
    logging.debug(f'Ticker {ticker} validated')
    return ticker

def get_price_from_service(ticker: str):
    ticker = validate_ticker(ticker)
    params = {
        'index_name': ticker.lower()
    }
    try:
        response = requests.get(DERIBIT_URL, params=params)
        response.raise_for_status()
    except HTTPError as e:
        logging.error(f'{str(e)}')
        return {'error': f'{str(e)}'}
    except ConnectionError as e:
        logging.error(f'{str(e)}')
        return {'error': f'{str(e)}'}
    except Timeout as e:
        logging.error(f'{str(e)}')
        return {'error': f'{str(e)}'}
    except RequestException as e:
        logging.error(f'{str(e)}')
        return {'error': f'{str(e)}'}
    data = response.json()
    if 'result' not in data or data['result'] is None:
        logging.error('No result from Deribit API')
        return {'error': 'No result from Deribit API'}
    logging.info(
        f'Data for {ticker} sucsessfully fetched from Deribit API.')
    return data['result']['index_price']

def get_prices_from_db(ticker: str, from_ts: int = None, to_ts: int = None):
    session = SessionLocal()
    query = session.query(PriceDB).filter(PriceDB.ticker==ticker)
    if from_ts is not None and to_ts is not None:
        query = query.filter(PriceDB.timestamp.between(from_ts, to_ts))
    result = query.all()
    session.close()
    logging.info(
        f'Prices for {ticker} from {from_ts} to {to_ts} got from database.')
    return [(r.price, r.timestamp) for r in result]

def get_latest_price_from_db(ticker: str):
    session = SessionLocal()
    query = (session.query(PriceDB)
             .filter(PriceDB.ticker==ticker)
             .order_by(PriceDB.timestamp.desc())
             .first())
    session.close()
    logging.info(f'Latest price for {ticker} got from database.')
    return query

def save_price(ticker: str, price: float, timestamp: int):
    session = SessionLocal()
    try:
        new_price = PriceDB(
            ticker=ticker,
            price=price,
            timestamp=timestamp
        )
        session.add(new_price)
        session.commit()
        logging.info(f'Saved price {price} for {ticker} at {timestamp}.')
    except Exception as e:
        session.rollback()
        logging.error(
            f'Failed to save price for {ticker}={price} at {timestamp}: {e}')
        raise e
    finally:
        session.close()
