import hashlib
import uuid
from datetime import datetime, date
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.models import Staffs, Cure, CureService
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


def get_all_staffs(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    staff_id: Optional[uuid.UUID] = None,
):
    if skip < 0:
        skip = 0
    query = db.query(Staffs).filter(Staffs.role == "doctor")

    if staff_id and staff_id != "undefined":
        query = query.filter(Staffs.id == staff_id)

    return query.offset(skip * limit).limit(limit).all()


def get_all_staff(db: Session, staff_id: Optional[uuid.UUID] = None):
    query = db.query(Staffs).filter(Staffs.role == "doctor")
    if staff_id:
        query.filter(Staffs.id == staff_id)
    return query.all()


def get_cures_for_salary(
    db: Session,
    filter_staff: Optional[uuid.UUID] = None,
    start_date_str: str = None,
    end_date_str: str = None,
):
    query = (
        db.query(Cure).filter(Cure.is_done == "Yakunlandi").filter(Cure.payed_price > 0)
    )
    if start_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
            start_date = datetime(start_date.year, start_date.month, start_date.day)
            query = query.filter(Cure.start_time >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = date.fromisoformat(end_date_str)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            query = query.filter(Cure.start_time <= end_date)
        except ValueError:
            pass
    if filter_staff and filter_staff != "undefined":
        query = query.filter(Staffs.id == filter_staff)
    return query.all()


def get_cures_for_statistic(
    db: Session,
    year_month: str = None,
):
    query = (
        db.query(Cure)
        .filter(Cure.is_done == "Yakunlandi")
        .filter(Cure.price == Cure.payed_price)
    )
    if year_month:
        year, month = map(int, year_month.split("-"))
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        query = query.filter(
            Cure.created_at >= start_date,
            Cure.created_at < end_date,
        )
    return query.all()


def get_cure_services_for_salary(db: Session):
    return db.query(CureService).all()


def count_staffs(
    db: Session,
    search: Optional[str] = None,
    current_user: dict = None,
):
    query = db.query(Staffs)
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(Staffs.name.ilike(search), Staffs.surname.ilike(search))
        )
    if current_user:
        query.filter(Staffs.id != current_user["id"])
    return query.count()


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
        foiz=staff.foiz,
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
    _staff.foiz = staff.foiz
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


def update_staff_image(db: Session, staff_image_url: str, staff_id: uuid.UUID):
    _staff = get_staff_by_id(db, staff_id)
    _staff.img_url = staff_image_url
    _staff.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_staff)
    return _staff


def update_staff_color(db: Session, staff_color: str, staff_id: uuid.UUID):
    _staff = get_staff_by_id(db, staff_id)
    _staff.color = staff_color
    _staff.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_staff)
    return _staff
