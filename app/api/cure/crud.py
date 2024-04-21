import datetime
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.api.models import Cure, Staffs, Users, CureService
from app.api.schemas import CureSchema


def get_cures(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Cure, Staffs, Users)
        .select_from(Cure)
        .join(Users, Cure.user_id == Users.id)
        .join(Staffs, Cure.staff_id == Staffs.id)
        .offset(skip)
        .limit(limit)
        .order_by(Cure.start_time.desc())
        .all()
    )


def get_cures_for_staff(
    db: Session, current_staff_id: uuid.UUID, skip: int = 0, limit: int = 10
):
    return (
        db.query(Cure, Staffs, Users)
        .select_from(Cure)
        .join(Users, Cure.user_id == Users.id)
        .join(Staffs, Cure.staff_id == Staffs.id)
        .filter(Cure.staff_id == current_staff_id)
        .offset(skip)
        .limit(limit)
        .order_by(Cure.start_time.desc())
        .all()
    )


def get_cure_by_id_for_staff(
    db: Session, cure_id: uuid.UUID, current_staff_id: uuid.UUID
):
    return (
        db.query(Cure, Users, Staffs)
        .select_from(Cure)
        .filter(cure_id == Cure.id)
        .join(Staffs, Staffs.id == current_staff_id)
        .first()
    )


def get_cure_by_id(db: Session, cure_id: uuid.UUID):
    return db.query(Cure).filter(cure_id == Cure.id).first()


def create_cure(db: Session, cure: CureSchema):
    _cure = Cure(
        staff_id=cure.staff_id,
        user_id=cure.user_id,
        start_time=cure.start_time,
        end_time=cure.end_time,
        img_url=cure.img_url,
        created_at=datetime.datetime.now().isoformat(),
    )
    db.add(_cure)
    db.commit()
    db.refresh(_cure)
    return _cure


def delete_cure(db: Session, cure_id: uuid.UUID):
    _cure = get_cure_by_id(db, cure_id)
    db.delete(_cure)
    db.commit()


def update_cure(db: Session, cure: CureSchema):
    _cure = get_cure_by_id(db, cure.id)
    _cure.name = cure.name
    _cure.surname = cure.surname
    _cure.job = cure.job
    _cure.date_birth = cure.date_birth
    _cure.address = cure.address
    _cure.updated_at = (datetime.datetime.now().isoformat(),)
    _cure.phone_number = cure.phone_number
    db.commit()
    db.refresh(_cure)
    return _cure


def end_cure(
    db: Session,
    cure_id: uuid.UUID,
    payload_services: List[uuid.UUID],
    payload: List[int],
):
    _cure = get_cure_by_id(db, cure_id)
    for tooth_id in payload:
        for service_id in payload_services:
            _cure_service = CureService(
                service_id=service_id, tooth_id=tooth_id, cure_id=_cure.id
            )
            db.add(_cure_service)
    _cure.updated_at = datetime.datetime.now()
    _cure.is_done = "Yakunlandi"
    db.commit()
    db.refresh(_cure)
    return _cure
