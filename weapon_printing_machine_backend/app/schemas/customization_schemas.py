# app/schemas/customization_schemas.py
from pydantic import BaseModel
from typing import List, Optional

class CustomizationCreate(BaseModel):
    weapon_id: int
    parts: List[int]  # IDs of the selected parts

class CustomizationResponse(BaseModel):
    id: int
    weapon_id: int
    parts: List[int]
    print_job_id: Optional[int]  # Include the ID of the print job created

    class Config:
        from_attributes = True
