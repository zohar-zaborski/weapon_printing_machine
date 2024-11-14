from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db  # Import get_db from database.py

router = APIRouter()

@router.post("/print", response_model=schemas.PrintJobResponse)
def send_to_print(customization_id: int, db: Session = Depends(get_db)):
    print_job = crud.create_print_job(db=db, customization_id=customization_id)
    if print_job is None:
        raise HTTPException(status_code=404, detail="Customization not found")
    return print_job

@router.get("/print/jobs", response_model=list[schemas.PrintJobResponse])
def get_all_print_jobs(db: Session = Depends(get_db)):
    return crud.get_all_print_jobs(db=db)

@router.get("/print/jobs/{job_id}", response_model=schemas.PrintJobResponse)
def get_print_job(job_id: int, db: Session = Depends(get_db)):
    print_job = crud.get_print_job_by_id(db=db, job_id=job_id)
    if print_job is None:
        raise HTTPException(status_code=404, detail="Print job not found")
    return print_job

@router.put("/print/jobs/{job_id}", response_model=schemas.PrintJobResponse)
def update_print_job_status(job_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_print_job_status(db=db, job_id=job_id, status=status)
