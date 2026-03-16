import logging

from fastapi import APIRouter, Query, HTTPException

from app.utils import (get_prices_from_db,
                    get_latest_price_from_db,
                    validate_ticker)
from app.schemas import PriceResponse

router = APIRouter()

@router.get('/prices', summary='Get all prices', tags=['Prices'])
def get_prices(ticker: str = Query(...), limit: int = Query(None)):
    ticker = validate_ticker(ticker)
    prices = get_prices_from_db(ticker)
    if limit is not None:
        prices = prices[:limit]
    prices_formated = [
        PriceResponse(ticker=ticker, price=price[0], timestamp=price[1])
        for price in prices
        ]
    logging.info(f'GET /prices?ticker={ticker}&limit={limit}')
    return {"prices": prices_formated}

@router.get('/prices/latest', summary='Get latest price', tags=['Prices'])
def get_latest_price(ticker: str = Query(...)):
    ticker = validate_ticker(ticker)
    price = get_latest_price_from_db(ticker)
    if price is None:
        raise HTTPException(status_code=404, detail='Ticker not found')
    logging.info(f'GET /prices/latest?ticker={ticker}')
    return PriceResponse(
        ticker=ticker,
        price=price.price,
        timestamp=price.timestamp
    )

@router.get(
    '/prices/filter', summary='Get prices in time period', tags=['Prices'])
def get_prices_by_date(
    ticker: str = Query(...),
    from_ts: int = Query(None),
    to_ts: int = Query(None)
    ):
    ticker = validate_ticker(ticker)
    prices = get_prices_from_db(ticker, from_ts, to_ts)
    prices_formated = [
        PriceResponse(ticker=ticker, price=price[0], timestamp=price[1])
        for price in prices
        ]
    logging.info(
        f'GET /prices/filter?ticker={ticker}&from_ts={from_ts}&to_ts={to_ts}')
    return {"prices": prices_formated}
