from pydantic import BaseModel
from typing import List, Optional

class UserLogin(BaseModel):
    username: str
    password: str

class SearchResult(BaseModel):
    symbol: str
    name: str
    price: float

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

class PortfolioItem(BaseModel):
    symbol: str
    quantity: int
    current_price: float

class Portfolio(BaseModel):
    user_id: str
    items: List[PortfolioItem]
  