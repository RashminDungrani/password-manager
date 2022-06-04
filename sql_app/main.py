from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        db.execute("PRAGMA foreign_keys=ON")
        yield db
    finally:
        db.close()


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_email(db, email=item.email)
    if db_item:
        raise HTTPException(status_code=400, detail="email already exist")

    db_item = crud.get_item_by_username(db, username=item.username)
    if db_item:
        raise HTTPException(status_code=400, detail="username already exist")

    return crud.create_item(db=db, item=item)


@app.delete("/domain/", response_model=list[schemas.Item])
def delete_items_by_domain(domain: str, db: Session = Depends(get_db)):
    domain_item = crud.get_domain_id_by_domain(db=db, domain=domain)
    if not domain_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    del_items = (
        db.query(models.Item).filter(models.Item.domain_id == domain_item.id).all()
    )
    # here we converting schema object to json data so that way it will not raise this exception
    # sqlalchemy.orm.exc.ObjectDeletedError: Instance '<Item at 0x1038dc4f0>' has been deleted, or its row is otherwise not present.
    json_data = jsonable_encoder(del_items)

    crud.delete_items_by_domain(db, domain_id=domain_item.id)

    return json_data
