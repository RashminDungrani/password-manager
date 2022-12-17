"""
third party table for storing creds that are registered with third party like google, apple, facebook, linkedin, github etc,
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    pass


class ThirdPartyCred(SQLModel, table=True):
    __tablename__: str = "ThirdPartyCred"
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    provider: str = Field(min_length=1, unique=True, nullable=False)
    name: Optional[str] = Field(min_length=1, nullable=True)
    mobile: Optional[str] = Field(min_length=8, nullable=True)
    email: EmailStr = Field(nullable=False)
    password: str = Field(min_length=4, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)
