from pydantic import BaseModel, EmailStr
from typing import Optional


# 🔐 --- Авторизация --- 🔐
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None

from typing import List

class CarBase(BaseModel):
    title: str
    description: str
    brand: str
    year: int
    image_url: str

class CarCreate(CarBase):
    pass

class CarOut(CarBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
