import hashlib
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Staffs
from app.api.schemas import StaffsSchema


def get_staff(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    current_user: dict = None,
    order_by=Optional[str],
    search: Optional[str] = None,
):
    if skip < 0:
        skip = 0

    query = db.query(Staffs)

    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(Staffs.name.ilike(search), Staffs.surname.ilike(search))
        )

    if order_by == "descend":
        query = query.order_by(Staffs.name.desc())
    elif order_by == "ascend":
        query = query.order_by(Staffs.name.asc())
    else:
        query = query.order_by(Staffs.created_at.desc())

    return (
        query.filter(Staffs.id != current_user["id"])
        .offset(skip * limit)
        .limit(limit)
        .all()
    )


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
        created_at=datetime.now().isoformat(),
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
    _staff.address = staff.address
    _staff.phone_number = staff.phone_number
    _staff.gender = staff.gender
    _staff.login = staff.login
    if staff.password:
        _staff.password = hashlib.sha256(staff.password.encode()).hexdigest()
    if staff.role:
        _staff.role = staff.role
    _staff.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_staff)
    return _staff


def update_me(db: Session, staff: StaffsSchema, staff_id: uuid.UUID):
    _staff = get_staff_by_id(db, staff_id)
    _staff.name = staff.name
    _staff.surname = staff.surname
    _staff.address = staff.address
    _staff.phone_number = staff.phone_number
    _staff.gender = staff.gender
    if staff.login:
        _staff.login = staff.login
    if staff.password:
        _staff.password = hashlib.sha256(staff.password.encode()).hexdigest()
    if staff.role:
        _staff.role = staff.role
    _staff.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_staff)
    return _staff
