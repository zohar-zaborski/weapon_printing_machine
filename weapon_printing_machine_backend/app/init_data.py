# app/init_data.py
from sqlalchemy.orm import Session
from .models import Weapon

def initialize_weapon_data(db):
    predefined_weapons = [
        {"name": "Assault Rifle", "compatible_parts": "1,2,3"},
        {"name": "Sniper Rifle", "compatible_parts": "2,4"},
        {"name": "Shotgun", "compatible_parts": "1,3,5"},
    ]

    for weapon in predefined_weapons:
        if not db.query(Weapon).filter(Weapon.name == weapon["name"]).first():
            db.add(Weapon(name=weapon["name"], compatible_parts=weapon["compatible_parts"]))
    db.commit()