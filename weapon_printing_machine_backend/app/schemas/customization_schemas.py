from pydantic import BaseModel, field_validator
from typing import List, Optional
from pydantic.config import ConfigDict


class CustomizationCreate(BaseModel):
    weapon_id: int
    parts: List[int]  # IDs of the selected parts

    model_config = ConfigDict(from_attributes=True)


class CustomizationResponse(BaseModel):
    id: int
    weapon_id: int
    parts: List[int]
    print_job_id: Optional[int]

    @field_validator("parts", mode="before")
    def split_parts(cls, value):
        # Convert comma-separated string to a list of integers
        if isinstance(value, str):
            return [int(part) for part in value.split(",")]
        return value

    model_config = ConfigDict(from_attributes=True)
