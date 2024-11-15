from pydantic import BaseModel
from pydantic.config import ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
