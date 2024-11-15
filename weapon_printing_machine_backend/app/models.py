from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Weapon(Base):
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    compatible_parts = Column(String)  # CSV of compatible part types

class WeaponPart(Base):
    __tablename__ = "weapon_parts"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    compatible_weapons = Column(String)  # CSV of compatible weapon names

class CustomizedWeapon(Base):
    __tablename__ = "customized_weapons"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weapon_id = Column(Integer, ForeignKey("weapons.id"))
    parts = Column(String)  # CSV of part IDs

    # Relationships
    user = relationship("User")
    weapon = relationship("Weapon")
    print_job = relationship(
        "PrintJob",
        back_populates="customized_weapon",
        foreign_keys="PrintJob.customized_weapon_id"  # Specify the foreign key
    )

class PrintJob(Base):
    __tablename__ = "print_jobs"
    id = Column(Integer, primary_key=True, index=True)
    customized_weapon_id = Column(Integer, ForeignKey("customized_weapons.id"))
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customized_weapon = relationship(
        "CustomizedWeapon",
        back_populates="print_job",
        foreign_keys="PrintJob.customized_weapon_id"  # Specify the foreign key
    )
