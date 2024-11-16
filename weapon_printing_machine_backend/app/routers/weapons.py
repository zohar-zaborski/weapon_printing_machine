from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .. import schemas, crud, auth_utils
from ..database import get_db  # Import get_db from database.py
from app.models import WeaponPart  # Import the SQLAlchemy model
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Retrieve the current authenticated user from the token.
    """
    payload = auth_utils.decode_access_token(token)
    username = payload.get("sub")
    user_id = payload.get("user_id")

    if not username or not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )
    return user

@router.get("/weapons", response_model=list[schemas.WeaponBase])
def get_weapons(
    db: Session = Depends(get_db), 
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """
    Get all weapons. Requires authentication.
    """
    return crud.get_all_weapons(db=db)

@router.get("/weapons/{weapon_id}", response_model=schemas.WeaponBase)
def get_weapon(
    weapon_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """
    Get a specific weapon by ID. Requires authentication.
    """
    weapon = crud.get_weapon_by_id(db=db, weapon_id=weapon_id)
    if weapon is None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon

@router.get("/parts", response_model=list[schemas.WeaponPart])
def get_parts(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """
    Get all weapon parts. Requires authentication.
    """
    weapon_parts = crud.get_all_parts(db=db)

    # Transform the compatible_weapons field from CSV to list
    transformed_parts = [
        schemas.WeaponPart(
            id=part.id,
            type=part.type,
            name=part.name,
            compatible_weapons=part.compatible_weapons.split(",")  # Convert CSV to list
        )
        for part in weapon_parts
    ]

    return transformed_parts


@router.get("/parts/{part_id}", response_model=schemas.WeaponPart)
def get_part_by_id(
    part_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific weapon part by ID.
    """
    # Use the SQLAlchemy model for querying
    part = db.query(WeaponPart).filter(WeaponPart.id == part_id).first()
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    # Transform the SQLAlchemy model to the Pydantic schema
    return WeaponPart(
        id=part.id,
        type=part.type,
        name=part.name,
        compatible_weapons=part.compatible_weapons.split(",")  # Convert CSV to list
    )