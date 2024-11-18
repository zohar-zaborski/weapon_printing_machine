# app/routers/customizations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth_utils import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Extract the user ID from the authenticated token.
    """
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id

# Create a new customization and optionally associate with a print job
@router.post("/", response_model=schemas.CustomizationResponse)
def customize_and_print(
    customization_data: schemas.CustomizationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    customization = crud.create_customization_and_print(
        db=db, customization_data=customization_data, user_id=user_id
    )
    return customization

@router.get("/", response_model=List[schemas.CustomizationResponse])
def get_all_customizations(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    customizations = crud.get_all_customizations(db, user_id=user_id)
    return customizations

@router.get("/{customization_id}", response_model=schemas.CustomizationResponse)
def get_customization(
    customization_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    customization = crud.get_customization_by_id(
        db=db, customization_id=customization_id, user_id=user_id
    )
    if customization is None:
        raise HTTPException(status_code=404, detail="Customization not found")
    return customization

@router.put("/{customization_id}", response_model=schemas.CustomizationResponse)
def update_customization(
    customization_id: int,
    customization: schemas.CustomizationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    updated_customization = crud.update_customization(
        db=db, customization_id=customization_id, customization=customization, user_id=user_id
    )
    if updated_customization is None:
        raise HTTPException(status_code=404, detail="Customization not found")
    return updated_customization

# Delete a customization by ID
@router.delete("/{customization_id}")
def delete_customization(
    customization_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    crud.delete_customization(db=db, customization_id=customization_id, user_id=user_id)
    return {"message": "Customization deleted successfully"}
