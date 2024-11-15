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
def create_customization_and_print(db: Session, customization_data: schemas.CustomizationCreate, user_id: int):
    # Create the customization
    db_customization = models.CustomizedWeapon(
        user_id=user_id,  # User ID from the token
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

    return {
        "id": db_customization.id,
        "weapon_id": db_customization.weapon_id,
        "parts": customization_data.parts,
        "print_job_id": db_print_job.id
    }


def get_all_customizations(db: Session, user_id: int):
    customizations = db.query(models.CustomizedWeapon).filter(
        models.CustomizedWeapon.user_id == user_id
    ).all()

    results = []
    for customization in customizations:
        # Convert parts from comma-separated string to list
        parts_list = list(map(int, customization.parts.split(",")))

        # Get the associated print job if it exists
        print_job = db.query(models.PrintJob).filter(
            models.PrintJob.customized_weapon_id == customization.id
        ).first()
        print_job_id = print_job.id if print_job else None

        results.append({
            "id": customization.id,
            "user_id": customization.user_id,
            "weapon_id": customization.weapon_id,
            "parts": parts_list,
            "print_job_id": print_job_id,
        })

    return results


def get_customization_by_id(db: Session, customization_id: int, user_id: int):
    customization = db.query(models.CustomizedWeapon).filter(
        models.CustomizedWeapon.id == customization_id,
        models.CustomizedWeapon.user_id == user_id
    ).first()

    if customization:
        # Convert parts from CSV to list
        parts_list = list(map(int, customization.parts.split(",")))

        # Get the associated print job
        print_job = db.query(models.PrintJob).filter(
            models.PrintJob.customized_weapon_id == customization.id
        ).first()
        print_job_id = print_job.id if print_job else None

        return {
            "id": customization.id,
            "user_id": customization.user_id,
            "weapon_id": customization.weapon_id,
            "parts": parts_list,
            "print_job_id": print_job_id,
        }

    return None

def update_customization(db: Session, customization_id: int, customization: schemas.CustomizationCreate, user_id: int):
    # Fetch the customization owned by the user
    db_customization = db.query(models.CustomizedWeapon).filter(
        models.CustomizedWeapon.id == customization_id,
        models.CustomizedWeapon.user_id == user_id
    ).first()

    if not db_customization:
        # Return None if customization doesn't exist or doesn't belong to the user
        return None

    # Update the customization fields
    db_customization.weapon_id = customization.weapon_id
    db_customization.parts = ",".join(map(str, customization.parts))  # Convert list to CSV format
    db.commit()
    db.refresh(db_customization)

    # Ensure the updated data matches the response model
    # Fetch associated print job if any
    print_job = db.query(models.PrintJob).filter(
        models.PrintJob.customized_weapon_id == customization_id
    ).first()
    print_job_id = print_job.id if print_job else None

    return {
        "id": db_customization.id,
        "user_id": db_customization.user_id,
        "weapon_id": db_customization.weapon_id,
        "parts": list(map(int, db_customization.parts.split(","))),
        "print_job_id": print_job_id,
    }



def delete_customization(db: Session, customization_id: int, user_id: int):
    db_customization = db.query(models.CustomizedWeapon).filter(
        models.CustomizedWeapon.id == customization_id,
        models.CustomizedWeapon.user_id == user_id
    ).first()
    if db_customization:
        db.delete(db_customization)
        db.commit()


# Print Job operations

# Print Job operations

def create_print_job(db: Session, customization_id: int, user_id: int):
    # Fetch the customization and check that it belongs to the user
    customization = db.query(models.CustomizedWeapon).filter(
        models.CustomizedWeapon.id == customization_id,
        models.CustomizedWeapon.user_id == user_id  # Ensure the customization belongs to the user
    ).first()
    
    if not customization:
        return None  # Handle missing customization or mismatch with the user
    
    # Create a new print job
    db_print_job = models.PrintJob(customized_weapon_id=customization_id)
    db.add(db_print_job)
    db.commit()
    db.refresh(db_print_job)
    return db_print_job



def get_all_print_jobs(db: Session, user_id: int):
    # Fetch all print jobs that belong to the user
    return db.query(models.PrintJob).join(models.CustomizedWeapon).filter(
        models.CustomizedWeapon.user_id == user_id  # Filter by the user's customizations
    ).all()


def get_print_job_by_id(db: Session, job_id: int, user_id: int):
    # Fetch a print job by ID and ensure it belongs to the user
    return db.query(models.PrintJob).join(models.CustomizedWeapon).filter(
        models.PrintJob.id == job_id,
        models.CustomizedWeapon.user_id == user_id  # Ensure the print job is linked to the user
    ).first()


def update_print_job_status(db: Session, job_id: int, status: str, user_id: int):
    # Fetch the print job and ensure it belongs to the user
    db_print_job = db.query(models.PrintJob).join(models.CustomizedWeapon).filter(
        models.PrintJob.id == job_id,
        models.CustomizedWeapon.user_id == user_id  # Ensure the print job belongs to the user
    ).first()
    
    if db_print_job:
        db_print_job.status = status
        db.commit()
        db.refresh(db_print_job)
    return db_print_job
