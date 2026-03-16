from pydantic import BaseModel
from typing import List


class PriceItem(BaseModel):
    ticker: str
    price: float
    timestamp: int


class PriceList(BaseModel):
    ticker: str
    prices: List[PriceItem]
