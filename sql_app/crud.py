from datetime import datetime

from sqlalchemy.orm import Session

from . import models as m
from . import schemas as s


# Item
def get_item_by_id(db: Session, id: int):
    return db.query(m.Item).filter(m.Item.id == id).first()


def get_items_by_domain_id(db: Session, domain_id: int):
    return db.query(m.Item).filter(m.Item.domain_id == domain_id).all()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(m.Item)
        .filter(m.Item.deleted_at == None)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_item_by_email(db: Session, email: str):
    return db.query(m.Item).filter(m.Item.email == email).first()


def get_item_by_username(db: Session, username: str):
    return db.query(m.Item).filter(m.Item.username == username).first()


def create_item(db: Session, item: s.ItemCreate, domain: m.Domain):

    db_item = m.Item(
        username=item.username,
        email=item.email,
        password=item.password,
        domain_id=domain.id,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item: m.Item) -> m.Item:
    item.deleted_at = datetime.now()
    db.commit()
    return item


def delete_items_by_domain(db: Session, domain: m.Domain, items: list[m.Item]):
    deleted_time = datetime.now()
    domain.deleted_at = deleted_time

    for item in items:
        item.deleted_at = deleted_time

    db.commit()


# domain
def create_domain(db: Session, domain: str) -> m.Domain:
    domain_item = m.Domain(domain=domain)
    db.add(domain_item)
    db.commit()
    db.refresh(domain_item)
    return domain_item


def get_domain_id_by_domain(db: Session, domain: str, except_deleted=False):
    return (
        db.query(m.Domain)
        .filter(
            m.Domain.domain == domain,
            (m.Domain.deleted_at == None if except_deleted else True),
        )
        .first()
    )


def update_domain_by_id(db: Session, domain: m.Domain, new_domain: str):
    domain.domain = new_domain
    domain.updated_at = datetime.now()
    db.commit()
    return domain
