import datetime
import uuid

from sqlalchemy import Column, UUID, String, DateTime, Integer, ForeignKey, Boolean

from app.db import Base, engine


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    date_birth = Column(DateTime, nullable=False)
    address = Column(String, nullable=False)
    img_url = Column(String, nullable=True)
    prikus = Column(String, nullable=True)
    disease_progression = Column(String, nullable=True)
    objective_check = Column(String, nullable=True)
    milk = Column(String, nullable=True)
    placental_diseases = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    job = Column(String, nullable=False)
    description = Column(String, nullable=True)
    balance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Staffs(Base):
    __tablename__ = "staffs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    address = Column(String, nullable=False)
    login = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    role = Column(String, default="doctor")
    color = Column(String, nullable=True)
    foiz = Column(Integer, nullable=False)
    img_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Cure(Base):
    __tablename__ = "cure"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID, ForeignKey("staffs.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    is_done = Column(String, default="Kutilmoqda")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    img_url = Column(String)
    price = Column(Integer, default=0)
    payed_price = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class CureService(Base):
    __tablename__ = "cure_service"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id = Column(UUID, ForeignKey("services.id"))
    service_name = Column(String, nullable=False)
    service_price = Column(Integer, nullable=False)
    tooth_id = Column(Integer, nullable=False)
    cure_id = Column(UUID, ForeignKey("cure.id"))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Services(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    service_category_id = Column(UUID, ForeignKey("services_category.id"))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class ServicesCategory(Base):
    __tablename__ = "services_category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Payments(Base):
    __tablename__ = "payment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Integer)
    payment_type_id = Column(UUID, ForeignKey("payment_type.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


class Payment_type(Base):
    __tablename__ = "payment_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


Base.metadata.create_all(bind=engine)
