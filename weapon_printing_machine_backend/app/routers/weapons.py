from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .. import schemas, crud, auth_utils
from ..database import get_db  # Import get_db from database.py

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    return crud.get_all_parts(db=db)

@router.get("/parts/{part_id}", response_model=schemas.WeaponPart)
def get_part(
    part_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """
    Get a specific weapon part by ID. Requires authentication.
    """
    part = crud.get_part_by_id(db=db, part_id=part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part
