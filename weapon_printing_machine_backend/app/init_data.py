# app/init_data.py
from sqlalchemy.orm import Session
from .models import Weapon

def initialize_weapon_data(db: Session):
    predefined_weapons = [
        Weapon(name="Assault Rifle", compatible_parts="scope,grip,magazine"),
        Weapon(name="Sniper Rifle", compatible_parts="scope,barrel"),
        Weapon(name="Shotgun", compatible_parts="barrel,stock"),
    ]
    for weapon in predefined_weapons:
        if not db.query(Weapon).filter(Weapon.name == weapon.name).first():
            db.add(weapon)
    db.commit()
