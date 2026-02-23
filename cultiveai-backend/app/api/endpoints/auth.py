from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ... import schemas, crud, models
from ...core import security
from .. import deps

router = APIRouter()


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """Register a new user."""
    db_user = crud.crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.crud_user.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.TokenPair)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login and get access + refresh tokens."""
    user = crud.crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return security.create_token_pair(subject=user.email)


@router.post("/refresh", response_model=schemas.TokenPair)
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(deps.get_db)
):
    """Get new access + refresh tokens using a valid refresh token."""
    email = security.verify_token(request.refresh_token, token_type="refresh")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.crud_user.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return security.create_token_pair(subject=user.email)


@router.get("/me", response_model=schemas.User)
def get_current_user_info(
    current_user: models.User = Depends(deps.get_current_user)
):
    """Get current authenticated user info."""
    return current_user


@router.put("/me", response_model=schemas.User)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update current user's profile."""
    if user_update.email and user_update.email != current_user.email:
        existing = crud.crud_user.get_user_by_email(db, email=user_update.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
    return crud.crud_user.update_user(db, db_user=current_user, user_update=user_update)