# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from .auth_utils import hash_password

# User operations
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Weapon and Part operations
def get_all_weapons(db: Session):
    return db.query(models.Weapon).all()

def get_weapon_by_id(db: Session, weapon_id: int):
    return db.query(models.Weapon).filter(models.Weapon.id == weapon_id).first()

def get_all_parts(db: Session):
    return db.query(models.WeaponPart).all()

def get_part_by_id(db: Session, part_id: int):
    return db.query(models.WeaponPart).filter(models.WeaponPart.id == part_id).first()

# Customization operations
def create_customization_and_print(db: Session, customization_data: schemas.CustomizationCreate):
    # Create the customization
    db_customization = models.CustomizedWeapon(
        weapon_id=customization_data.weapon_id,
        parts=",".join(map(str, customization_data.parts))
    )
    db.add(db_customization)
    db.commit()
    db.refresh(db_customization)

    # Create the associated print job
    db_print_job = models.PrintJob(customized_weapon_id=db_customization.id)
    db.add(db_print_job)
    db.commit()
    db.refresh(db_print_job)

    # Return both customization and print job details
    return {
        "id": db_customization.id,
        "weapon_id": db_customization.weapon_id,
        "parts": customization_data.parts,
        "print_job_id": db_print_job.id
    }

def get_all_customizations(db: Session):
    customizations = db.query(models.CustomizedWeapon).all()
    results = []
    for customization in customizations:
        # Convert parts from comma-separated string to list
        parts_list = list(map(int, customization.parts.split(",")))
        
        # Get the associated print job if it exists
        print_job = db.query(models.PrintJob).filter(models.PrintJob.customized_weapon_id == customization.id).first()
        print_job_id = print_job.id if print_job else None

        # Append the result in the expected format
        results.append({
            "id": customization.id,
            "user_id": customization.user_id,
            "weapon_id": customization.weapon_id,
            "parts": parts_list,
            "print_job_id": print_job_id
        })
    return results

def get_customization_by_id(db: Session, customization_id: int):
    return db.query(models.CustomizedWeapon).filter(models.CustomizedWeapon.id == customization_id).first()

def update_customization(db: Session, customization_id: int, customization: schemas.CustomizationCreate):
    db_customization = db.query(models.CustomizedWeapon).filter(models.CustomizedWeapon.id == customization_id).first()
    if db_customization:
        db_customization.weapon_id = customization.weapon_id
        db_customization.parts = ",".join(map(str, customization.parts))
        db.commit()
        db.refresh(db_customization)
    return db_customization

def delete_customization(db: Session, customization_id: int):
    db_customization = db.query(models.CustomizedWeapon).filter(models.CustomizedWeapon.id == customization_id).first()
    if db_customization:
        db.delete(db_customization)
        db.commit()

# Print Job operations
def create_print_job(db: Session, customization_id: int):
    db_print_job = models.PrintJob(customized_weapon_id=customization_id)
    db.add(db_print_job)
    db.commit()
    db.refresh(db_print_job)
    return db_print_job

def get_all_print_jobs(db: Session):
    return db.query(models.PrintJob).all()

def get_print_job_by_id(db: Session, job_id: int):
    return db.query(models.PrintJob).filter(models.PrintJob.id == job_id).first()

def update_print_job_status(db: Session, job_id: int, status: str):
    db_print_job = db.query(models.PrintJob).filter(models.PrintJob.id == job_id).first()
    if db_print_job:
        db_print_job.status = status
        db.commit()
        db.refresh(db_print_job)
    return db_print_job
