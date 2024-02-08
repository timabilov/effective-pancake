
import sqlalchemy as sa
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from database import Base


class Catalog(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        """Returns table name  by lowercasing a Class name"""
        return cls.__name__.lower()

    pk = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(256), nullable=False)
    size = sa.Column(sa.String(256), nullable=False)
    color = sa.Column(sa.String(256), nullable=False)
    price = sa.Column(sa.Float(), nullable=False)
    brand = sa.Column(sa.String(256), nullable=False)
    category = sa.Column(sa.String(256), nullable=False)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
