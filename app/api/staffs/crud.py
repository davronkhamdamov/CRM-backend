import hashlib
import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.models import Staffs
from app.api.schemas import StaffsSchema


def get_staff(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Staffs).offset(skip).limit(limit).all()


def count_staffs(db: Session):
    return db.query(func.count(Staffs.id)).scalar()


def get_staff_by_id(db: Session, staff_id: uuid.UUID):
    return db.query(Staffs).filter(Staffs.id == staff_id).first()


def create_staff(db: Session, staff: StaffsSchema):
    _staff = Staffs(
        name=staff.name,
        surname=staff.surname,
        address=staff.address,
        login=staff.login,
        password=hashlib.sha256(staff.password.encode()).hexdigest(),
        phone_number=staff.phone_number,
        gender=staff.gender,
        role=staff.role,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(_staff)
    db.commit()
    db.refresh(_staff)
    return _staff


def delete_staff(db: Session, staff_id: uuid.UUID):
    _staff = get_staff_by_id(db, staff_id)
    db.delete(_staff)
    db.commit()


def update_staff(db: Session, staff: StaffsSchema):
    _staff = get_staff_by_id(db, staff.id)
    _staff.name = staff.name
    _staff.surname = staff.surname
    _staff.date_birth = staff.date_birth
    _staff.address = staff.address
    _staff.phone_number = staff.phone_number
    _staff.gender = staff.gender
    _staff.role = staff.role
    _staff.updated_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(_staff)
    return _staff


# hashed_entered_password = hashlib.sha256(entered_password.encode()).hexdigest()
#
# # Compare hashed_entered_password with stored hashed_password
# if hashed_entered_password == hashed_password:
#     print("Password is correct!")
# else:
#     print("Incorrect password.")
