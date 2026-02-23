from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas


def get_client(db: Session, client_id: int, owner_id: int) -> Optional[models.Client]:
    return db.query(models.Client).filter(
        models.Client.id == client_id,
        models.Client.owner_id == owner_id
    ).first()


def get_clients(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[models.Client]:
    query = db.query(models.Client).filter(models.Client.owner_id == owner_id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Client.name.ilike(search_filter)) |
            (models.Client.document.ilike(search_filter)) |
            (models.Client.email.ilike(search_filter)) |
            (models.Client.city.ilike(search_filter))
        )

    return query.order_by(models.Client.name).offset(skip).limit(limit).all()


def get_clients_count(db: Session, owner_id: int, search: Optional[str] = None) -> int:
    query = db.query(func.count(models.Client.id)).filter(models.Client.owner_id == owner_id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Client.name.ilike(search_filter)) |
            (models.Client.document.ilike(search_filter)) |
            (models.Client.email.ilike(search_filter)) |
            (models.Client.city.ilike(search_filter))
        )

    return query.scalar()


def create_client(db: Session, client: schemas.ClientCreate, owner_id: int) -> models.Client:
    db_client = models.Client(
        **client.model_dump(),
        owner_id=owner_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(
    db: Session,
    db_client: models.Client,
    client_update: schemas.ClientUpdate
) -> models.Client:
    update_data = client_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, db_client: models.Client) -> None:
    db.delete(db_client)
    db.commit()


def get_client_properties_count(db: Session, client_id: int) -> int:
    return db.query(func.count(models.Property.id)).filter(
        models.Property.client_id == client_id
    ).scalar()
