from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ... import schemas, crud, models
from .. import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Client])
def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """List all clients for the current user with optional search."""
    clients = crud.crud_client.get_clients(
        db, owner_id=current_user.id, skip=skip, limit=limit, search=search
    )
    # Add properties count
    for client in clients:
        client.properties_count = crud.crud_client.get_client_properties_count(db, client.id)
    return clients


@router.get("/count")
def get_clients_count(
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Get total count of clients."""
    count = crud.crud_client.get_clients_count(db, owner_id=current_user.id, search=search)
    return {"count": count}


@router.get("/{client_id}", response_model=schemas.Client)
def get_client(
    client_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Get a specific client by ID."""
    client = crud.crud_client.get_client(db, client_id=client_id, owner_id=current_user.id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    client.properties_count = crud.crud_client.get_client_properties_count(db, client.id)
    return client


@router.post("/", response_model=schemas.Client, status_code=status.HTTP_201_CREATED)
def create_client(
    client: schemas.ClientCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Create a new client."""
    db_client = crud.crud_client.create_client(db, client=client, owner_id=current_user.id)
    db_client.properties_count = 0
    return db_client


@router.put("/{client_id}", response_model=schemas.Client)
def update_client(
    client_id: int,
    client_update: schemas.ClientUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update a client."""
    db_client = crud.crud_client.get_client(db, client_id=client_id, owner_id=current_user.id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    updated = crud.crud_client.update_client(db, db_client=db_client, client_update=client_update)
    updated.properties_count = crud.crud_client.get_client_properties_count(db, updated.id)
    return updated


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Delete a client and all its properties."""
    db_client = crud.crud_client.get_client(db, client_id=client_id, owner_id=current_user.id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    crud.crud_client.delete_client(db, db_client=db_client)
    return None
