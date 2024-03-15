import uuid
from datetime import datetime
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class UserSchema(BaseModel):
    id: uuid.UUID | None = None
    name: str = None
    surname: str = None
    date_birth: datetime = None
    address: str = None
    phone_number: str = None
    gender: str = None
    job: str = None
    balance: int = None
    created_at: datetime = None
    updated_at: datetime = None


class Staffs(BaseModel):
    id: uuid.UUID = None
    name: str = None
    surname: str = None
    date_birth: datetime = None
    address: str = None
    phone_number: str = None
    gender: str = None
    role: str = None
    created_at: datetime = None
    updated_at: datetime = None


class Cure(BaseModel):
    __tablename__ = "cure"

    id: uuid.UUID = None
    staff_id: uuid.UUID = None
    service_id: uuid.UUID = None
    user_id: uuid.UUID = None
    is_done: str = None
    start_time: str = None
    end_time: str = None
    img_url: str = None
    tooth_id: str = None
    created_at: datetime = None
    updated_at: datetime | None = None


class Services(BaseModel):
    id: uuid.UUID = None
    name: str = None
    price: int = None
    raw_material_price: int = None
    service_price_price: int = None
    created_at: datetime = None
    updated_at: datetime | None = None


class Tooth(BaseModel):
    id: uuid.UUID = None
    tooth_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: datetime | None = None


class Payments(BaseModel):
    id: uuid.UUID = None
    amount: int = None
    payment_type_id: uuid.UUID = None
    user_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: datetime | None = None


class Payment_type(BaseModel):
    id: uuid.UUID = None
    method: str = None
    created_at: datetime = None
    updated_at: datetime | None = None


class Response(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T] = None
