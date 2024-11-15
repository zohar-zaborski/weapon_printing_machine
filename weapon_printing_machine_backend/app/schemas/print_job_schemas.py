from pydantic import BaseModel
from datetime import datetime
from pydantic.config import ConfigDict


class PrintJobResponse(BaseModel):
    id: int
    customized_weapon_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
