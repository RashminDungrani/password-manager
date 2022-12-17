"""
third party table for storing creds that are registered with third party like google, apple, facebook, linkedin, github etc,
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.credential_model import Credential


class ThirdPartyInput(SQLModel):
    signup_cred_id: int = Field(foreign_key="Credential.id", nullable=False)
    signup_with_third_party_cred_id: int = Field(foreign_key="Credential.id", nullable=False)


class ThirdParty(ThirdPartyInput, table=True):
    __tablename__: str = "ThirdParty"

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    signup_cred: "Credential" = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="ThirdParty.signup_cred_id==Credential.id")
    )
    signup_with_third_party_cred: "Credential" = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="ThirdParty.signup_with_third_party_cred_id==Credential.id")
    )
