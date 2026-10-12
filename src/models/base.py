from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData

from core.config import settings


class Base(DeclarativeBase):
    pass
