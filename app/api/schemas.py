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
    balance: int | None = None
    created_at: datetime = None
    updated_at: datetime = None


class StaffsSchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    surname: str = None
    address: str = None
    login: str | None = None
    password: str | None = None
    phone_number: str = None
    gender: str = None
    role: str = None
    created_at: datetime = None
    updated_at: datetime = None


class CureSchema(BaseModel):
    __tablename__ = "cure"

    id: uuid.UUID | None = None
    staff_id: uuid.UUID = None
    service_id: uuid.UUID = None
    user_id: uuid.UUID = None
    is_done: str | None = None
    start_time: str = None
    end_time: str = None
    img_url: str = None
    tooth_id: str = None
    created_at: datetime = None
    updated_at: datetime | None = None


class ServicesSchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    price: int = None
    status: bool = None
    raw_material_price: int = None
    service_price_price: int = None
    created_at: datetime = None
    updated_at: datetime | None = None


class ToothSchema(BaseModel):
    id: uuid.UUID = None
    tooth_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: datetime | None = None


class PaymentsSchema(BaseModel):
    id: uuid.UUID = None
    amount: int = None
    payment_type_id: uuid.UUID = None
    user_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: datetime | None = None


class PaymentTypeSchema(BaseModel):
    id: uuid.UUID = None
    method: str = None
    created_at: datetime = None
    updated_at: datetime | None = None


class Response(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    total: int | None = None
    result: Optional[T] = None
    info: dict | None = None


class LoginSchema(BaseModel):
    login: str
    password: str
