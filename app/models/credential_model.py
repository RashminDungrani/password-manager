"""
Credential table
"""
import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr, validator
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.domain_model import Domain


class CredentialInput(SQLModel):
    domain_id: int = Field(foreign_key="Domain.id", nullable=False)
    username: Optional[str] = Field(index=True, min_length=1, nullable=True)
    email: Optional[EmailStr] = Field(index=True, nullable=True)
    mobile: Optional[str] = Field(min_length=8, nullable=True)
    password: Optional[str] = Field(min_length=2, nullable=True)
    pin: Optional[int] = Field(gt=999, nullable=True)
    third_party_cred_id: Optional[int] = Field(foreign_key="ThirdParty.id", nullable=True)
    note: Optional[str] = Field(min_length=1, nullable=True)

    # @validator("*")
    # def empty_str_to_none(cls, v):
    #     if v == "":
    #         return None
    #     return v


class Credential(CredentialInput, table=True):
    __tablename__: str = "Credential"

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    # TODO: Validation username and email and third_party_id all can not be null
    # TODO: Validation password and pin both can not be null

    domain: "Domain" = Relationship(back_populates="credentials")  # child


class CredentialReadWithDomain(CredentialInput):
    id: int
    created_at: datetime
    modified_at: datetime
    deleted_at: Optional[datetime]

    domain: "Domain"
