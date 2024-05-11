import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.models import Cure, Staffs, Users, CureService, Services, Payments
from app.api.schemas import CureSchema, updateCure, PaymentsSchema
from app.api.users.crud import get_user_by_id


def get_cures(db: Session, staff_id: uuid.UUID = None):
    query = (
        db.query(Cure, Staffs, Users)
        .select_from(Cure)
        .join(Users, Cure.user_id == Users.id)
        .join(Staffs, Cure.staff_id == Staffs.id)
    )
    if staff_id != "undefined" and staff_id:
        query = query.filter(Staffs.id == staff_id)
    return query.order_by(Cure.start_time.desc()).all()


def get_cure_with_service(db: Session, cure_id: uuid.UUID):
    return (
        db.query(CureService, Services)
        .join(CureService, CureService.service_id == Services.id)
        .filter(CureService.cure_id == cure_id)
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
        .order_by(Cure.is_done.asc())
        .order_by(Cure.start_time.asc())
        .offset(skip * limit)
        .limit(limit)
        .all()
    )


def get_cures_for_staff_by_id(
    db: Session, staff_id: uuid.UUID, skip: int = 0, limit: int = 10
):
    return (
        db.query(Cure, Staffs, Users)
        .select_from(Cure)
        .join(Users, Cure.user_id == Users.id)
        .join(Staffs, Cure.staff_id == Staffs.id)
        .order_by(Cure.start_time.desc())
        .filter(Cure.staff_id == staff_id)
        .offset(skip * limit)
        .limit(limit)
        .all()
    )


def get_cures_for_patient(
    db: Session, patient_id: uuid.UUID, skip: int = 0, limit: int = 10
):
    return (
        db.query(Cure, Staffs, Users)
        .select_from(Cure)
        .join(Users, Cure.user_id == Users.id)
        .join(Staffs, Cure.staff_id == Staffs.id)
        .filter(Cure.user_id == patient_id)
        .order_by(Cure.start_time.desc())
        .offset(skip * limit)
        .limit(limit)
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
    print(cure.start_time)
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


def count_cure_for_staff(db: Session, staff_id: uuid.UUID):
    return db.query(func.count(Cure.id)).filter(Cure.staff_id == staff_id).scalar()


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
    cure: updateCure,
    is_done: str,
):
    _cure = get_cure_by_id(db, cure_id)
    for tooth in cure.payload_services:
        for services in tooth["services"]:
            _cure_service = CureService(
                service_id=services, tooth_id=tooth["id"], cure_id=_cure.id
            )
            db.add(_cure_service)
    _cure.updated_at = datetime.datetime.now()
    _cure.price = cure.price
    _cure.is_done = is_done
    db.commit()
    db.refresh(_cure)
    return _cure


def pay_with_balance_cure(db: Session, cure_id: uuid.UUID, cure: updateCure):
    _cure = get_cure_by_id(db, cure_id)
    _user = get_user_by_id(db, _cure.user_id)
    _user.balance -= cure.price
    _cure.updated_at = datetime.datetime.now()
    _cure.payed_price += cure.price
    db.commit()
    db.refresh(_cure)
    return _cure


def pay_with_cash_cure(db: Session, cure_id: uuid.UUID, payment: PaymentsSchema):
    _cure = get_cure_by_id(db, cure_id)
    _user = get_user_by_id(db, _cure.user_id)
    _payment = Payments(
        amount=payment.amount,
        payment_type_id=payment.payment_type_id,
        user_id=_user.id,
        created_at=datetime.datetime.now().isoformat(),
    )
    db.add(_payment)
    _cure.payed_price += payment.amount
    _cure.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(_cure)
    return _cure
