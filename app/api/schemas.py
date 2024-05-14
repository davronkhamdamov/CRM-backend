import uuid
from datetime import datetime
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class UserSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    surname: str = None
    date_birth: datetime = None
    address: str = None
    phone_number: str = None
    gender: str = None
    job: str = None
    prikus: Optional[str] = None
    disease_progression: Optional[str] = None
    objective_check: Optional[str] = None
    milk: Optional[str] = None
    placental_diseases: Optional[str] = None
    description: Optional[str] = None
    balance: Optional[str] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class StaffsSchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    surname: str = None
    address: str = None
    login: Optional[str] = None
    password: Optional[str] = None
    phone_number: str = None
    gender: str = None
    role: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class CureSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    staff_id: uuid.UUID = None
    service_id: uuid.UUID = None
    user_id: uuid.UUID = None
    is_done: Optional[str] = None
    start_time: str = None
    end_time: str = None
    img_url: str = None
    tooth_id: str = None
    price: Optional[int] = None
    payed_price: Optional[int] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class ServicesSchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    price: int = None
    service_category_id: uuid.UUID
    status: bool = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class ServicesCategorySchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class ToothSchema(BaseModel):
    id: uuid.UUID = None
    tooth_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class PaymentsSchema(BaseModel):
    id: uuid.UUID = None
    amount: int = None
    payment_type_id: uuid.UUID = None
    user_id: uuid.UUID = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class PaymentTypeSchema(BaseModel):
    id: uuid.UUID = None
    method: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class Response(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    total: Optional[int] = None
    result: Optional[T] = None
    info: Optional[dict] = None
    role: Optional[str] = None


class LoginSchema(BaseModel):
    login: str
    password: str


class updateCure(BaseModel, Generic[T]):
    payload_services: Optional[T] = None
    is_done: Optional[str] = None
    price: Optional[int] = None


class Prikus(BaseModel):
    prikus: str


class Status(BaseModel):
    status: str
