from sqlalchemy.orm import Session
from .models import User, Weapon, WeaponPart
from .auth_utils import hash_password  # Import the password hashing utility

def initialize_weapon_data(db: Session):
    predefined_weapons = [
        {"name": "Glock 17", "compatible_parts": "1,4,7,10"},
        {"name": "M4", "compatible_parts": "2,3,5,8,11"},
        {"name": "FN Minimi", "compatible_parts": "3,6,9,12"},
    ]

    for weapon in predefined_weapons:
        if not db.query(Weapon).filter(Weapon.name == weapon["name"]).first():
            db.add(Weapon(name=weapon["name"], compatible_parts=weapon["compatible_parts"]))
    db.commit()

def initialize_weapon_parts_data(db: Session):
    predefined_parts = [
        {"id": 1, "type": "Sight", "name": "Mepro - MPO PRO", "compatible_weapons": "Glock 17"},
        {"id": 2, "type": "Sight", "name": "Mepro - Hunter 4x", "compatible_weapons": "M4"},
        {"id": 3, "type": "Sight", "name": "Mepro - MMX 3", "compatible_weapons": "M4,FN Minimi"},
        {"id": 4, "type": "Laser Pointer", "name": "Nightstick - TSM11G", "compatible_weapons": "Glock 17"},
        {"id": 5, "type": "Laser Pointer", "name": "Wilcox - RAAM GSS", "compatible_weapons": "M4"},
        {"id": 6, "type": "Laser Pointer", "name": "Wilcox - Raid Xe", "compatible_weapons": "FN Minimi"},
        {"id": 7, "type": "Grip Handle", "name": "MCK - Micro Conversion Kit Gen 2", "compatible_weapons": "Glock 17"},
        {"id": 8, "type": "Grip Handle", "name": "Law - Grip-Pod Forgerip", "compatible_weapons": "M4"},
        {"id": 9, "type": "Grip Handle", "name": "BravoCo - Vertical Grip Mod 3", "compatible_weapons": "FN Minimi"},
        {"id": 10, "type": "Barrel Attachment", "name": "Banish - Banish 45", "compatible_weapons": "Glock 17"},
        {"id": 11, "type": "Barrel Attachment", "name": "Midwest - Muzzle Break", "compatible_weapons": "M4"},
        {"id": 12, "type": "Barrel Attachment", "name": "Midwest - Blast Diverter", "compatible_weapons": "FN Minimi"},
    ]

    for part in predefined_parts:
        existing_part = db.query(WeaponPart).filter(WeaponPart.name == part["name"]).first()
        if not existing_part:
            # Add part to the database
            db.add(WeaponPart(
                id=part["id"],  # Specify the ID if required
                type=part["type"],
                name=part["name"],
                compatible_weapons=part["compatible_weapons"]
            ))
        elif existing_part:
            # Update existing part if needed
            existing_part.type = part["type"]
            existing_part.compatible_weapons = part["compatible_weapons"]

    db.commit()

def initialize_admin_user(db: Session):
    """
    Ensure an admin user exists in the database. If not, create one.
    """
    admin_username = "admin"
    admin_password = "admin"  # Default password for demonstration purposes

    existing_admin = db.query(User).filter(User.username == admin_username).first()
    if not existing_admin:
        hashed_password = hash_password(admin_password)
        admin_user = User(
            username=admin_username,
            email="admin@example.com",
            password=hashed_password,
        )
        db.add(admin_user)
        db.commit()
        
   
        