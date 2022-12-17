from datetime import datetime
from typing import Optional

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, select

from app.db.dependencies import get_db_session
from app.models.domain_model import Domain


class DomainDAO:
    """Class for accessing Domain table."""

    def __init__(self, session: Session = get_db_session()) -> None:
        self.session = session

    def __del__(self) -> None:
        self.session.close()

    def select_one(self, domain_id: int) -> Domain:
        domain = self.session.get(Domain, domain_id)
        if not domain:
            raise Exception("domain id not found")

        return domain

    def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[Domain]:
        query = select(Domain).offset(offset).limit(limit)
        domains = (self.session.execute(query)).scalars().all()
        return domains

    def insert(self, domain_input: str) -> Domain:
        try:
            domain: Domain = Domain(domain_name=domain_input)
            self.session.add(domain)
            self.session.commit()
            return domain
        except exc.IntegrityError as error:
            print(error.code, error.params)
            self.session.rollback()
            raise Exception(f"Domain id does not exist")

    def update(self, db_domain: Domain, updated_domain: str) -> Domain:
        db_domain.domain_name = updated_domain
        db_domain.modified_at = datetime.now()
        self.session.add(db_domain)
        self.session.commit()
        self.session.refresh(db_domain)

        return db_domain

    def delete(self, domain_item: Domain) -> None:
        self.session.delete(domain_item)
        self.session.commit()

    def delete_all(self) -> None:
        query = delete(Domain)
        self.session.execute(query)
        self.session.commit()
