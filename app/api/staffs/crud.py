import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.models import Staffs
from app.api.schemas import StaffsSchema


def get_staff(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Staffs).offset(skip).limit(limit).all()


def get_staff_by_id(db: Session, staff_id: uuid.UUID):
    return db.query(Staffs).filter(Staffs.id == staff_id).first()


def create_staff(db: Session, staff: StaffsSchema):
    _staff = Staffs(
        name=staff.name,
        surname=staff.surname,
        date_birth=staff.date_birth,
        address=staff.address,
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
