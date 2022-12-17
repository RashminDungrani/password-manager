from datetime import datetime
from typing import Optional

from sqlalchemy import exc
from sqlmodel import Session, delete, select

from app.db.dependencies import get_db_session
from app.models.third_party_model import ThirdParty, ThirdPartyInput


class ThirdPartyDAO:
    """Class for accessing third party table."""

    def __init__(self, session: Session = get_db_session()) -> None:
        self.session = session

    def __del__(self) -> None:
        self.session.close()

    def select_one(self, third_party_id: int) -> ThirdParty:
        third_party = self.session.get(ThirdParty, third_party_id)
        if not third_party:
            raise Exception("third_party id not found")

        return third_party

    def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[ThirdParty]:
        query = select(ThirdParty).offset(offset).limit(limit)
        third_partys = (self.session.execute(query)).scalars().all()
        return third_partys

    def insert(self, third_party_input: ThirdPartyInput) -> ThirdParty:
        try:
            third_party: ThirdParty = ThirdParty.from_orm(third_party_input)
            self.session.add(third_party)
            self.session.commit()
            self.session.refresh(third_party)
            return third_party
        except exc.IntegrityError as error:
            print(error.code, error.params)
            self.session.rollback()
            raise Exception(f"ThirdParty id does not exist")

    def update(self, db_third_party: ThirdParty, updated_third_party: str) -> ThirdParty:
        db_third_party.third_party_name = updated_third_party
        db_third_party.modified_at = datetime.now()
        self.session.add(db_third_party)
        self.session.commit()
        self.session.refresh(db_third_party)

        return db_third_party

    def delete(self, third_party_item: ThirdParty) -> None:
        self.session.delete(third_party_item)
        self.session.commit()

    def delete_all(self) -> None:
        query = delete(ThirdParty)
        self.session.execute(query)
        self.session.commit()
