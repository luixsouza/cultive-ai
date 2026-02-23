from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas


def get_property(db: Session, property_id: int, owner_id: int) -> Optional[models.Property]:
    return db.query(models.Property).join(models.Client).filter(
        models.Property.id == property_id,
        models.Client.owner_id == owner_id
    ).first()


def get_properties(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    client_id: Optional[int] = None,
    search: Optional[str] = None
) -> List[models.Property]:
    query = db.query(models.Property).join(models.Client).filter(
        models.Client.owner_id == owner_id
    )

    if client_id:
        query = query.filter(models.Property.client_id == client_id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Property.name.ilike(search_filter)) |
            (models.Property.city.ilike(search_filter)) |
            (models.Client.name.ilike(search_filter))
        )

    return query.order_by(models.Property.name).offset(skip).limit(limit).all()


def get_properties_count(
    db: Session,
    owner_id: int,
    client_id: Optional[int] = None,
    search: Optional[str] = None
) -> int:
    query = db.query(func.count(models.Property.id)).join(models.Client).filter(
        models.Client.owner_id == owner_id
    )

    if client_id:
        query = query.filter(models.Property.client_id == client_id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Property.name.ilike(search_filter)) |
            (models.Property.city.ilike(search_filter)) |
            (models.Client.name.ilike(search_filter))
        )

    return query.scalar()


def create_property(
    db: Session,
    property_data: schemas.PropertyCreate,
    owner_id: int
) -> Optional[models.Property]:
    # Verify client belongs to owner
    client = db.query(models.Client).filter(
        models.Client.id == property_data.client_id,
        models.Client.owner_id == owner_id
    ).first()

    if not client:
        return None

    db_property = models.Property(**property_data.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def update_property(
    db: Session,
    db_property: models.Property,
    property_update: schemas.PropertyUpdate
) -> models.Property:
    update_data = property_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_property, field, value)
    db.commit()
    db.refresh(db_property)
    return db_property


def delete_property(db: Session, db_property: models.Property) -> None:
    db.delete(db_property)
    db.commit()


def get_property_reports_count(db: Session, property_id: int) -> int:
    return db.query(func.count(models.AnalysisReport.id)).filter(
        models.AnalysisReport.property_id == property_id
    ).scalar()
