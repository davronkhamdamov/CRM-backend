import datetime
import uuid

from sqlalchemy import Column, UUID, String, DateTime, Integer, ForeignKey

from app.db import Base, engine


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    date_birth = Column(DateTime, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    job = Column(String, nullable=False)
    balance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


class Staffs(Base):
    __tablename__ = "staffs"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    date_birth = Column(DateTime, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    role = Column(String, default="doctor")
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


class Cure(Base):
    __tablename__ = "cure"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    staff_id = Column(UUID)
    service_id = Column(UUID)
    user_id = Column(UUID)
    is_done = Column(String)
    start_time = Column(DateTime, default=datetime.UTC)
    end_time = Column(DateTime, nullable=True)
    img_url = Column(String)
    tooth_id = Column(UUID)
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


class Services(Base):
    __tablename__ = "services"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    raw_material_price = Column(Integer, nullable=False)
    service_price_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


class Tooth(Base):
    __tablename__ = "tooth"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    tooth_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


class Payments(Base):
    __tablename__ = "payment"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    amount = Column(Integer)
    payment_type_id = Column(UUID, ForeignKey("payment_type.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


class Payment_type(Base):
    __tablename__ = "payment_type"

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    method = Column(String)
    created_at = Column(DateTime, default=datetime.UTC)
    updated_at = Column(DateTime)


Base.metadata.create_all(bind=engine)
