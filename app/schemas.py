from pydantic import BaseModel


class PriceResponse(BaseModel):
    ticker: str
    price: float
    timestamp: int
