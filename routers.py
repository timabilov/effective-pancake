

from models.base import Catalog
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from deps import get_session
from schema import CatalogFilterQuery, CatalogItemsOut


core = APIRouter(
    tags=['Core'],
    prefix='',
)


@core.get('/catalog', response_model=CatalogItemsOut)
async def catalog(
        # We can make our schema more strict by adding enums, check field string sizes etc.
        f: CatalogFilterQuery = Depends(),
        session: Session = Depends(get_session),
):
    """API for returning and filtering catalog data"""
    q = session.query(Catalog)
    if f.name:
        q = q.filter(Catalog.name == f.name)
    if f.size:
        q = q.filter(Catalog.size == f.size)
    if f.color:
        q = q.filter(Catalog.color == f.color)
    if f.category:
        q = q.filter(Catalog.category == f.category)
    if f.brand:
        q = q.filter(Catalog.brand == f.brand)

    return CatalogItemsOut.model_validate(
        {'items': q.order_by(Catalog.created_at.desc()).all()}
    )
