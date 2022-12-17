"""
Domain table
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import AnyUrl
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    pass


class Domain(SQLModel, table=True):
    __tablename__: str = "domain"

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    domain_url: AnyUrl = Field(index=True, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    # TODO: Add Relation on credential table
