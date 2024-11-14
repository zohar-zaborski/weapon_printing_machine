from pydantic import BaseModel, validator
from typing import List


class WeaponBase(BaseModel):
    name: str
    compatible_parts: List[str]  # Expecting a list for the response

    @validator("compatible_parts", pre=True)
    def split_compatible_parts(cls, value):
        # If compatible_parts is a string, split it by commas into a list
        if isinstance(value, str):
            return value.split(",")
        return value

class WeaponPart(BaseModel):
    type: str
    name: str
    compatible_weapons: List[str]
