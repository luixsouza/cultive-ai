from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ... import schemas, crud, models
from .. import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.PropertyWithClient])
def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    client_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """List all properties for the current user with optional filters."""
    properties = crud.crud_property.get_properties(
        db, owner_id=current_user.id, skip=skip, limit=limit,
        client_id=client_id, search=search
    )
    result = []
    for prop in properties:
        prop_data = {
            "id": prop.id,
            "name": prop.name,
            "total_area_hectares": prop.total_area_hectares,
            "geojson_boundary": prop.geojson_boundary,
            "city": prop.city,
            "state": prop.state,
            "notes": prop.notes,
            "created_at": prop.created_at,
            "updated_at": prop.updated_at,
            "client_id": prop.client_id,
            "client_name": prop.client.name if prop.client else None,
            "reports_count": crud.crud_property.get_property_reports_count(db, prop.id)
        }
        result.append(schemas.PropertyWithClient(**prop_data))
    return result


@router.get("/count")
def get_properties_count(
    client_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Get total count of properties."""
    count = crud.crud_property.get_properties_count(
        db, owner_id=current_user.id, client_id=client_id, search=search
    )
    return {"count": count}


@router.get("/{property_id}", response_model=schemas.PropertyWithClient)
def get_property(
    property_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Get a specific property by ID."""
    prop = crud.crud_property.get_property(db, property_id=property_id, owner_id=current_user.id)
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    prop_data = {
        "id": prop.id,
        "name": prop.name,
        "total_area_hectares": prop.total_area_hectares,
        "geojson_boundary": prop.geojson_boundary,
        "city": prop.city,
        "state": prop.state,
        "notes": prop.notes,
        "created_at": prop.created_at,
        "updated_at": prop.updated_at,
        "client_id": prop.client_id,
        "client_name": prop.client.name if prop.client else None,
        "reports_count": crud.crud_property.get_property_reports_count(db, prop.id)
    }
    return schemas.PropertyWithClient(**prop_data)


@router.post("/", response_model=schemas.Property, status_code=status.HTTP_201_CREATED)
def create_property(
    property_data: schemas.PropertyCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Create a new property."""
    db_property = crud.crud_property.create_property(
        db, property_data=property_data, owner_id=current_user.id
    )
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client_id or client does not belong to you"
        )
    db_property.reports_count = 0
    return db_property


@router.put("/{property_id}", response_model=schemas.Property)
def update_property(
    property_id: int,
    property_update: schemas.PropertyUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update a property."""
    db_property = crud.crud_property.get_property(
        db, property_id=property_id, owner_id=current_user.id
    )
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    updated = crud.crud_property.update_property(
        db, db_property=db_property, property_update=property_update
    )
    updated.reports_count = crud.crud_property.get_property_reports_count(db, updated.id)
    return updated


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Delete a property and all its reports."""
    db_property = crud.crud_property.get_property(
        db, property_id=property_id, owner_id=current_user.id
    )
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    crud.crud_property.delete_property(db, db_property=db_property)
    return None
