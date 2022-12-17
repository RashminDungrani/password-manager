"""
Domain table
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import AnyUrl
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.credential_model import Credential


class Domain(SQLModel, table=True):
    __tablename__: str = "Domain"

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    domain_name: str = Field(index=True, unique=True, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    credentials: list["Credential"] = Relationship(back_populates="domain")  # parent
