from sqlalchemy.orm import Session

from . import models, schemas


# Item
def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item_by_email(db: Session, email: str):
    return db.query(models.Item).filter(models.Item.email == email).first()


def get_item_by_username(db: Session, username: str):
    return db.query(models.Item).filter(models.Item.username == username).first()


def create_item(db: Session, item: schemas.ItemCreate):
    domain_item = (
        db.query(models.Domain).filter(models.Domain.domain == item.domain_url).first()
    )

    if not domain_item:
        domain_item = models.Domain(domain=item.domain_url)
        db.add(domain_item)
        db.commit()
        db.refresh(domain_item)

    db_item = models.Item(
        username=item.username,
        email=item.email,
        password=item.password,
        domain_id=domain_item.id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_items_by_domain(db: Session, domain_id: int) -> list[schemas.Item]:
    # TODO: set deleted_at and while reading ignore those entries
    db.query(models.Domain).filter(models.Domain.id == domain_id).delete(
        synchronize_session="fetch"
    )

    db.commit()
    return []


# domain
def get_domain_id_by_domain(db: Session, domain: str):
    return db.query(models.Domain).filter(models.Domain.domain == domain).first()
