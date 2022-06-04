from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import crud
from . import models as m
from . import schemas as s
from .database import SessionLocal, engine

m.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        db.execute("PRAGMA foreign_keys=ON")
        yield db
    finally:
        db.close()


@app.get("/items/", response_model=list[s.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/items/", response_model=s.Item)
def create_item(item: s.ItemCreate, db: Session = Depends(get_db)):
    if (item.email == None and item.username == None) or (
        item.email == "" and item.username == ""
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please either provide username or email",
        )

    if item.email is not None:
        db_item = crud.get_item_by_email(db, email=item.email)
        if db_item:
            raise HTTPException(status_code=400, detail="email already exist")

    if item.username is not None:
        db_item = crud.get_item_by_username(db, username=item.username)
        if db_item:
            raise HTTPException(status_code=400, detail="username already exist")

    db_domain = crud.get_domain_id_by_domain(db, domain=item.domain_url)

    if db_domain and db_domain.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"domain url was deleted at the time of {db_domain.deleted_at}. use other domain or recover this domain",
        )

    if not db_domain:
        db_domain = crud.create_domain(db, domain=item.domain_url)

    return crud.create_item(db=db, item=item, domain=db_domain)


@app.patch("/update-domain", response_model=s.DomainResponse)
def update_domain(old_domain: str, new_domain: str, db: Session = Depends(get_db)):
    domain = crud.get_domain_id_by_domain(db, old_domain)

    if not domain:
        raise HTTPException(status_code=404, detail="Domain not exist")

    domain = crud.update_domain_by_id(db, domain, new_domain)

    return domain


@app.delete("/delete-item", response_model=s.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not exist")

    if item.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Item already deleted at {item.deleted_at}",
        )

    return crud.delete_item(db=db, item=item)


@app.delete("/domain-with-items/", response_model=list[s.Item])
def delete_items_with_domain(domain: str, db: Session = Depends(get_db)):
    domain_item = crud.get_domain_id_by_domain(db=db, domain=domain)
    if not domain_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="domain not found"
        )

    del_items = crud.get_items_by_domain_id(db, domain_item.id)
    if not del_items:
        del_items = []
    # here we converting schema object to json data so that way it will not raise this exception
    # sqlalchemy.orm.exc.ObjectDeletedError: Instance '<Item at 0x1038dc4f0>' has been deleted, or its row is otherwise not present.
    json_data = jsonable_encoder(del_items)

    crud.delete_items_by_domain(db, domain=domain_item, items=del_items)

    return json_data
