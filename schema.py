
from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel, ConfigDict



class CatalogFilterQuery(BaseModel):
    """Catalog filter query"""

    name: Optional[str] = Query(None)
    size: Optional[str] = Query(None)
    color: Optional[str] = Query(None)
    category: Optional[int] = Query(None)
    brand: Optional[str] = Query(None)


class CatalogItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    size: str
    color: str
    price: float
    brand: str
    category: str


class CatalogItemsOut(BaseModel):
    """Catalog filter query"""
    items: List[CatalogItemOut]
