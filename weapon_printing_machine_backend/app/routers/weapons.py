from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db  # Import get_db from database.py

router = APIRouter()


@router.get("/weapons", response_model=list[schemas.WeaponBase])
def get_weapons(db: Session = Depends(get_db)):
    return crud.get_all_weapons(db=db)

@router.get("/weapons/{weapon_id}", response_model=schemas.WeaponBase)
def get_weapon(weapon_id: int, db: Session = Depends(get_db)):
    weapon = crud.get_weapon_by_id(db=db, weapon_id=weapon_id)
    if weapon is None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon

@router.get("/parts", response_model=list[schemas.WeaponPart])
def get_parts(db: Session = Depends(get_db)):
    return crud.get_all_parts(db=db)

@router.get("/parts/{part_id}", response_model=schemas.WeaponPart)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = crud.get_part_by_id(db=db, part_id=part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part
