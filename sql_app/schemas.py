from datetime import datetime
from typing import Union

from pydantic import BaseModel


# Password Item
class ItemBase(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    password: str


class ItemCreate(ItemBase):
    domain_url: str


class Item(ItemBase):
    id: int
    domain_id: int
    is_active: bool
    created_at: datetime
    updatet_at: Union[datetime, None]
    deleted_at: Union[datetime, None]

    class Config:
        orm_mode = True


# Domain
class DomainBase(BaseModel):
    domain: str


class DomainCreate(DomainBase):
    pass


class Domain(BaseModel):
    id: int
