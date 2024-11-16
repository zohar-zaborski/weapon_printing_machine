from pydantic import BaseModel, field_validator
from typing import List
from pydantic.config import ConfigDict


class WeaponBase(BaseModel):
    name: str
    compatible_parts: List[str]

    @field_validator("compatible_parts", mode="before")
    def split_compatible_parts(cls, value):

        if isinstance(value, str):
            return value.split(",")
        return value

    model_config = ConfigDict(from_attributes=True)


class WeaponPart(BaseModel):
    id: int
    type: str
    name: str
    compatible_weapons: List[str]

    model_config = ConfigDict(from_attributes=True)
