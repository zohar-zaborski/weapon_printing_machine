# app/schemas/print_job_schemas.py
from pydantic import BaseModel
from datetime import datetime

class PrintJobResponse(BaseModel):
    id: int
    customized_weapon_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
