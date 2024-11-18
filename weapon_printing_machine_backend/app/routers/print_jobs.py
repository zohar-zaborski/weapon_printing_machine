from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .. import schemas, crud, auth_utils
from ..database import get_db
from typing import List

router = APIRouter()

# OAuth2 scheme to retrieve the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Dependency to retrieve the current user from the token
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

# Create a print job for a customization
@router.post("/print", response_model=schemas.PrintJobResponse)
def send_to_print(
    customization_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),  
):
    user_id = current_user.id  # Extract user ID from token
    customization = crud.get_customization_by_id(db=db, customization_id=customization_id, user_id=user_id)
    if customization is None:
        raise HTTPException(status_code=404, detail="Customization not found")
    
    
    print_job = crud.create_print_job(db=db, customization_id=customization_id, user_id=user_id)
    return print_job

@router.get("/jobs", response_model=List[schemas.PrintJobResponse])
def get_all_print_jobs(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),  
):
    user_id = current_user.id  # Extract user ID from token
    print_jobs = crud.get_all_print_jobs(db=db, user_id=user_id)
    return print_jobs

# Get a specific print job by ID
@router.get("/{job_id}", response_model=schemas.PrintJobResponse)
def get_print_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),  # Ensure user is authenticated
):
    user_id = current_user.id  # Extract user ID from token
    # Fetch the specific print job and check that it belongs to the correct user
    print_job = crud.get_print_job_by_id(db=db, job_id=job_id, user_id=user_id)
    if print_job is None:
        raise HTTPException(status_code=404, detail="Print job not found")
    return print_job

# Update the status of a specific print job
@router.put("/{job_id}", response_model=schemas.PrintJobResponse)
def update_print_job_status(
    job_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),  # Ensure user is authenticated
):
    user_id = current_user.id  # Extract user ID from token
    # Update the print job's status for the specific user
    updated_print_job = crud.update_print_job_status(db=db, job_id=job_id, status=status, user_id=user_id)
    if updated_print_job is None:
        raise HTTPException(status_code=404, detail="Print job not found")
    return updated_print_job
