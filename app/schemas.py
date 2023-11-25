from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class ContactResponse(BaseModel):
    contacts: List[Contact]

    class Config:
        schema_extra = {
            "example": {
                "contacts": [
                    {
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "1234567890",
                        "birthday": "1990-01-01",
                        "additional_data": "Some additional data"
                    },
                    {
                        "id": 2,
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "email": "jane.smith@example.com",
                        "phone_number": "9876543210",
                        "birthday": "1985-05-15",
                        "additional_data": "More additional data"
                    }
                ]
            }
        }

class ContactSearch(BaseModel):
    query: str

class ContactBirthdaySearch(BaseModel):
    days: int


class RequestEmail(BaseModel):
    email: EmailStr