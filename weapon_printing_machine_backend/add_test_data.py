# add_test_data.py
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models import CustomizedWeapon, PrintJob

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def add_test_data(db: Session):
    test_customizations = [
        {"weapon_id": 1, "parts": "1,2,3"},
        {"weapon_id": 2, "parts": "2,4"},
        {"weapon_id": 3, "parts": "1,3,5"},
    ]

    for customization_data in test_customizations:
        # Add customization
        db_customization = CustomizedWeapon(
            weapon_id=customization_data["weapon_id"],
            parts=customization_data["parts"]  # Store parts as a comma-separated string
        )
        db.add(db_customization)
        db.commit()
        db.refresh(db_customization)

        # Create a print job for the customization
        db_print_job = PrintJob(customized_weapon_id=db_customization.id)
        db.add(db_print_job)
        db.commit()
        db.refresh(db_print_job)



# Run the script
if __name__ == "__main__":
    db = SessionLocal()
    try:
        add_test_data(db)
    finally:
        db.close()
