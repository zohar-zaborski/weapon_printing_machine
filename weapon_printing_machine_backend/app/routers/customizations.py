from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db  # Import get_db from database.py
from typing import List
router = APIRouter()


@router.post("/customize", response_model=schemas.CustomizationResponse)
def customize_and_print(
    customization_data: schemas.CustomizationCreate, 
    db: Session = Depends(get_db)
):
    result = crud.create_customization_and_print(db=db, customization_data=customization_data)
    return result

@router.get("/customize", response_model=List[schemas.CustomizationResponse])
def get_all_customizations(db: Session = Depends(get_db)):
    customizations = crud.get_all_customizations(db)
    return customizations

@router.get("/customize/{customization_id}", response_model=schemas.CustomizationResponse)
def get_customization(customization_id: int, db: Session = Depends(get_db)):
    customization = crud.get_customization_by_id(db=db, customization_id=customization_id)
    if customization is None:
        raise HTTPException(status_code=404, detail="Customization not found")
    return customization

@router.put("/customize/{customization_id}", response_model=schemas.CustomizationResponse)
def update_customization(customization_id: int, customization: schemas.CustomizationCreate, db: Session = Depends(get_db)):
    return crud.update_customization(db=db, customization_id=customization_id, customization=customization)

@router.delete("/customize/{customization_id}")
def delete_customization(customization_id: int, db: Session = Depends(get_db)):
    crud.delete_customization(db=db, customization_id=customization_id)
    return {"message": "Customization deleted successfully"}
