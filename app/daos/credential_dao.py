from datetime import datetime
from typing import Optional

import typer
from sqlalchemy import exc
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.credential_model import (
    Credential,
    CredentialInput,
    CredentialReadWithDomain,
)


class CredentialDAO:
    """Class for accessing Credential table."""

    def __init__(self, session: Session = get_db_session()) -> None:
        self.session = session

    def __del__(self) -> None:
        self.session.close()

    def select_one(self, credential_id: int) -> Credential:
        credential = self.session.get(Credential, credential_id)
        if not credential:
            typer.secho("credential id not found")
            raise typer.Exit()

        return credential

    def select_one_with_domain(self, credential_id: int) -> CredentialReadWithDomain:
        query = select(Credential).where(Credential.id == credential_id).options(selectinload(Credential.domain))
        credential = (self.session.execute(query)).scalar_one_or_none()
        if not credential:
            typer.secho("credential id not found")
            raise typer.Exit()

        return credential

    def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[Credential]:
        query = select(Credential).offset(offset).limit(limit)
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_filter_by_domain_id(
        self, domain_id: int, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[Credential]:
        query = select(Credential).where(Credential.domain_id == domain_id).offset(offset).limit(limit)
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_all_with_domain(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CredentialReadWithDomain]:
        query = select(Credential).options(selectinload(Credential.domain)).offset(offset).limit(limit)
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_under_x_domain_with_domain(
        self, domain_id: int, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CredentialReadWithDomain]:
        query = (
            select(Credential)
            .where(Credential.domain_id == domain_id)
            .options(selectinload(Credential.domain))
            .offset(offset)
            .limit(limit)
        )
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_all_third_party_with_domain(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CredentialReadWithDomain]:
        query = (
            select(Credential)
            .where(Credential.third_party_cred_id != None)
            .options(selectinload(Credential.domain))
            .offset(offset)
            .limit(limit)
        )
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_by_username_and_domain(
        self, domain_id: int, username: str, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[Credential]:
        query = (
            select(Credential)
            .where(Credential.domain_id == domain_id, Credential.username == username)
            .offset(offset)
            .limit(limit)
        )
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_by_username(
        self, username: str, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CredentialReadWithDomain]:
        query = (
            select(Credential)
            .where(Credential.username.ilike("%" + username + "%"))  # type: ignore
            .options(selectinload(Credential.domain))
            .offset(offset)
            .limit(limit)
        )
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_by_email(
        self, email: str, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CredentialReadWithDomain]:
        query = (
            select(Credential)
            .where(Credential.email.ilike("%" + email + "%"))  # type: ignore
            .options(selectinload(Credential.domain))
            .offset(offset)
            .limit(limit)
        )
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def select_by_mobile(
        self, mobile: str, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CredentialReadWithDomain]:
        query = (
            select(Credential)
            .where(Credential.mobile.ilike("%" + mobile + "%"))  # type: ignore
            .options(selectinload(Credential.domain))
            .offset(offset)
            .limit(limit)
        )
        credentials = (self.session.execute(query)).scalars().all()
        return credentials

    def insert(self, inserted_credential: CredentialInput) -> Credential:
        try:
            credential: Credential = Credential.from_orm(inserted_credential)
            self.session.add(credential)
            self.session.commit()
            self.session.refresh(credential)
            return credential
        except exc.IntegrityError as error:
            print(error.code, error.params)
            self.session.rollback()
            raise Exception(f"Domain id {inserted_credential.domain_id} does not exist")

    def update(self, db_credential: Credential, updated_credential: CredentialInput) -> Credential:

        for key, value in (updated_credential.dict(exclude_unset=True)).items():
            setattr(db_credential, key, value)
        self.session.add(db_credential)
        self.session.commit()
        self.session.refresh(db_credential)

        return db_credential

    def delete(self, credential_item: Credential) -> None:
        self.session.delete(credential_item)
        self.session.commit()
