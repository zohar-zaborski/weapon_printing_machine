# app/routers/print_jobs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth_utils import get_current_user  # Import the utility function for token-based user authentication
from typing import List

router = APIRouter()

# Create a print job for a customization
@router.post("/print", response_model=schemas.PrintJobResponse)
def send_to_print(
    customization_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # Ensure user is authenticated
):
    user_id = current_user["user_id"]  # Extract user ID from token
    customization = crud.get_customization_by_id(db=db, customization_id=customization_id, user_id=user_id)
    if customization is None:
        raise HTTPException(status_code=404, detail="Customization not found")
    print_job = crud.create_print_job(db=db, customization_id=customization_id)
    return print_job

# Get all print jobs for the authenticated user
@router.get("/print/jobs", response_model=List[schemas.PrintJobResponse])
def get_all_print_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # Ensure user is authenticated
):
    user_id = current_user["user_id"]  # Extract user ID from token
    print_jobs = crud.get_all_print_jobs(db=db, user_id=user_id)
    return print_jobs

# Get a specific print job by ID
@router.get("/print/jobs/{job_id}", response_model=schemas.PrintJobResponse)
def get_print_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # Ensure user is authenticated
):
    user_id = current_user["user_id"]  # Extract user ID from token
    print_job = crud.get_print_job_by_id(db=db, job_id=job_id, user_id=user_id)
    if print_job is None:
        raise HTTPException(status_code=404, detail="Print job not found")
    return print_job

# Update the status of a specific print job
@router.put("/print/jobs/{job_id}", response_model=schemas.PrintJobResponse)
def update_print_job_status(
    job_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # Ensure user is authenticated
):
    user_id = current_user["user_id"]  # Extract user ID from token
    updated_print_job = crud.update_print_job_status(db=db, job_id=job_id, status=status, user_id=user_id)
    if updated_print_job is None:
        raise HTTPException(status_code=404, detail="Print job not found")
    return updated_print_job
