import datetime
import uuid
from datetime import date

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import OrtoCure, Staffs, Users, OrtaCureService, Services, Payments
from app.api.schemas import OrtoCureSchema, updateCure, PaymentsSchema
from app.api.users.crud import get_user_by_id


def get_cures(
    db: Session,
    staff_id: uuid.UUID = None,
    start_date_str: str = None,
    end_date_str: str = None,
    filters=None,
    skip: int = 0,
    limit: int = 10,
):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, Staffs.id == OrtoCure.staff_id)
    )
    if filters["status"] and filters["status"] != [""]:
        query = query.filter(OrtoCure.is_done.in_(filters["status"]))
    if len(filters["pay"]):
        for pay in filters["pay"]:
            if pay == "payed":
                query = query.filter(
                    or_(
                        OrtoCure.payed_price == OrtoCure.price,
                        OrtoCure.price < OrtoCure.payed_price,
                    )
                ).filter(OrtoCure.is_done == "Yakunlandi")
            elif pay == "not_fully_payed":
                query = (
                    query.filter(OrtoCure.payed_price > 0)
                    .filter(OrtoCure.price != OrtoCure.payed_price)
                    .filter(OrtoCure.price > OrtoCure.payed_price)
                )
            elif pay == "not_payed":
                query = query.filter(OrtoCure.payed_price == 0).filter(
                    OrtoCure.is_done == "Yakunlandi"
                )
            elif pay == "waiting":
                query = (
                    query.filter(OrtoCure.payed_price == 0)
                    .filter(OrtoCure.is_done == "Kutilmoqda")
                    .filter(OrtoCure.price == 0)
                )

    if start_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
            start_date = datetime.datetime(
                start_date.year, start_date.month, start_date.day
            )
            query = query.filter(OrtoCure.start_time >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = date.fromisoformat(end_date_str)
            end_date = datetime.datetime(
                end_date.year, end_date.month, end_date.day, 23, 59, 59
            )
            query = query.filter(OrtoCure.start_time <= end_date)
        except ValueError:
            pass
    if staff_id != "undefined" and staff_id:
        query = query.filter(Staffs.id == staff_id)
    return (
        query.order_by(OrtoCure.is_done == "Bekor qilingan")
        .order_by(OrtoCure.created_at.desc())
        .offset(skip * limit)
        .limit(limit)
        .all()
    )


def get_cures_for_schedule(
    db: Session,
    staff_id: uuid.UUID = None,
):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, Staffs.id == OrtoCure.staff_id)
    )

    if staff_id != "undefined" and staff_id:
        query = query.filter(Staffs.id == staff_id)
    return query.all()


def get_cures_count(
    db: Session,
    staff_id: uuid.UUID = None,
    start_date_str: str = None,
    end_date_str: str = None,
    filters=None,
):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, OrtoCure.staff_id == Staffs.id)
    )
    if filters["status"] and filters["status"] != [""]:
        query = query.filter(OrtoCure.is_done.in_(filters["status"]))
    if len(filters["pay"]):
        for pay in filters["pay"]:
            if pay == "payed":
                query = query.filter(
                    or_(
                        OrtoCure.payed_price == OrtoCure.price,
                        OrtoCure.price < OrtoCure.payed_price,
                    )
                ).filter(OrtoCure.is_done == "Yakunlandi")
            elif pay == "not_fully_payed":
                query = (
                    query.filter(OrtoCure.payed_price > 0)
                    .filter(OrtoCure.price != OrtoCure.payed_price)
                    .filter(OrtoCure.price > OrtoCure.payed_price)
                )
            elif pay == "not_payed":
                query = query.filter(OrtoCure.payed_price == 0).filter(
                    OrtoCure.is_done == "Yakunlandi"
                )
            elif pay == "waiting":
                query = (
                    query.filter(OrtoCure.payed_price == 0)
                    .filter(OrtoCure.is_done == "Kutilmoqda")
                    .filter(OrtoCure.price == 0)
                )
    if start_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
            start_date = datetime.datetime(
                start_date.year, start_date.month, start_date.day
            )
            query = query.filter(OrtoCure.start_time >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = date.fromisoformat(end_date_str)
            end_date = datetime.datetime(
                end_date.year, end_date.month, end_date.day, 23, 59, 59
            )
            query = query.filter(OrtoCure.start_time <= end_date)
        except ValueError:
            pass
    if staff_id != "undefined" and staff_id:
        query = query.filter(Staffs.id == staff_id)
    return query.order_by(OrtoCure.start_time.desc()).count()


def get_debt_cures(db: Session, staff_id: uuid.UUID = None):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, OrtoCure.staff_id == Staffs.id)
        .filter(OrtoCure.price > OrtoCure.payed_price)
    )
    if staff_id != "undefined" and staff_id:
        query = query.filter(Staffs.id == staff_id)
    return query.order_by(OrtoCure.start_time.desc()).all()


def get_cure_with_service(db: Session, cure_id: uuid.UUID):
    return (
        db.query(OrtaCureService, Services)
        .join(OrtaCureService, OrtaCureService.service_id == Services.id)
        .filter(OrtaCureService.cure_id == cure_id)
        .all()
    )


def get_cures_for_staff(
    db: Session,
    current_staff_id: uuid.UUID,
    start_date_str: str = None,
    end_date_str: str = None,
    skip: int = 0,
    limit: int = 10,
    filters=None,
):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, OrtoCure.staff_id == Staffs.id)
        .filter(OrtoCure.staff_id == current_staff_id)
        .order_by(
            OrtoCure.is_done == "Bekor qilingan",
        )
        .order_by(OrtoCure.created_at.desc())
    )
    if start_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
            start_date = datetime.datetime(
                start_date.year, start_date.month, start_date.day
            )
            query = query.filter(OrtoCure.start_time >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = date.fromisoformat(end_date_str)
            end_date = datetime.datetime(
                end_date.year, end_date.month, end_date.day, 23, 59, 59
            )
            query = query.filter(OrtoCure.start_time <= end_date)
        except ValueError:
            pass

    if filters["status"] and filters["status"] != [""]:
        query = query.filter(OrtoCure.is_done.in_(filters["status"]))
    if len(filters["pay"]):
        for pay in filters["pay"]:
            if pay == "payed":
                query = query.filter(
                    or_(
                        OrtoCure.payed_price == OrtoCure.price,
                        OrtoCure.price < OrtoCure.payed_price,
                    )
                ).filter(OrtoCure.is_done == "Yakunlandi")
            elif pay == "not_fully_payed":
                query = (
                    query.filter(OrtoCure.payed_price > 0)
                    .filter(OrtoCure.price != OrtoCure.payed_price)
                    .filter(OrtoCure.price > OrtoCure.payed_price)
                )
            elif pay == "not_payed":
                query = query.filter(OrtoCure.payed_price == 0).filter(
                    OrtoCure.is_done == "Yakunlandi"
                )
            elif pay == "waiting":
                query = (
                    query.filter(OrtoCure.payed_price == 0)
                    .filter(OrtoCure.is_done == "Kutilmoqda")
                    .filter(OrtoCure.price == 0)
                )

    return query.offset(skip * limit).limit(limit).all()


def get_cures_for_staff_count(db: Session, current_staff_id: uuid.UUID, filters=None):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, OrtoCure.staff_id == Staffs.id)
        .filter(OrtoCure.staff_id == current_staff_id)
    )

    if filters["status"] and filters["status"] != [""]:
        query = query.filter(OrtoCure.is_done.in_(filters["status"]))
    if len(filters["pay"]):
        for pay in filters["pay"]:
            if pay == "payed":
                query = query.filter(
                    or_(
                        OrtoCure.payed_price == OrtoCure.price,
                        OrtoCure.price < OrtoCure.payed_price,
                    )
                ).filter(OrtoCure.is_done == "Yakunlandi")
            elif pay == "not_fully_payed":
                query = (
                    query.filter(OrtoCure.payed_price > 0)
                    .filter(OrtoCure.price != OrtoCure.payed_price)
                    .filter(OrtoCure.price > OrtoCure.payed_price)
                )
            elif pay == "not_payed":
                query = query.filter(OrtoCure.payed_price == 0).filter(
                    OrtoCure.is_done == "Yakunlandi"
                )
            elif pay == "waiting":
                query = (
                    query.filter(OrtoCure.payed_price == 0)
                    .filter(OrtoCure.is_done == "Kutilmoqda")
                    .filter(OrtoCure.price == 0)
                )

    return query.count()


def get_cures_for_staff_by_id(
    db: Session,
    staff_id: uuid.UUID,
    skip: int = 0,
    limit: int = 10,
):
    query = (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, OrtoCure.staff_id == Staffs.id)
        .order_by(OrtoCure.start_time.desc())
    ).filter(OrtoCure.staff_id == staff_id)

    return query.offset(skip * limit).limit(limit).all()


def get_cures_for_patient(
    db: Session, patient_id: uuid.UUID, skip: int = 0, limit: int = 10
):
    return (
        db.query(OrtoCure, Staffs, Users)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, OrtoCure.staff_id == Staffs.id)
        .filter(OrtoCure.user_id == patient_id)
        .order_by(OrtoCure.start_time.desc())
        .offset(skip * limit)
        .limit(limit)
        .all()
    )


def get_cure_by_id_for_staff(
    db: Session, cure_id: uuid.UUID, current_staff_id: uuid.UUID
):
    return (
        db.query(OrtoCure, Users, Staffs)
        .select_from(OrtoCure)
        .join(Users, OrtoCure.user_id == Users.id)
        .join(Staffs, Staffs.id == OrtoCure.staff_id)
        .filter(cure_id == OrtoCure.id)
        .first()
    )


def get_cure_by_id(db: Session, cure_id: uuid.UUID):
    return db.query(OrtoCure).filter(cure_id == OrtoCure.id).first()


def create_cure(db: Session, cure: OrtoCureSchema):
    _cure = OrtoCure(
        staff_id=cure.staff_id,
        user_id=cure.user_id,
        start_time=datetime.datetime.strptime(cure.start_time, "%Y-%m-%d %H-%M-%S"),
        end_time=datetime.datetime.strptime(cure.end_time, "%Y-%m-%d %H-%M-%S"),
        img_url=cure.img_url,
        technic_name=cure.technic_name,
        created_at=datetime.datetime.now().isoformat(),
    )
    db.add(_cure)
    db.commit()
    db.refresh(_cure)
    return _cure


def count_cure_for_staff(db: Session, staff_id: uuid.UUID):
    return (
        db.query(func.count(OrtoCure.id)).filter(OrtoCure.staff_id == staff_id).scalar()
    )


def delete_cure(db: Session, cure_id: uuid.UUID):
    db.query(OrtaCureService).filter(OrtoCure.id == OrtaCureService.cure_id).delete()
    _cure = get_cure_by_id(db, cure_id)
    db.delete(_cure)
    db.commit()


def update_cure(db: Session, cure: OrtoCureSchema):
    _cure = get_cure_by_id(db, cure.id)
    _cure.name = cure.name
    _cure.surname = cure.surname
    _cure.job = cure.job
    _cure.date_birth = cure.date_birth
    _cure.address = cure.address
    _cure.updated_at = (datetime.datetime.now().isoformat(),)
    _cure.phone_number = cure.phone_number
    _cure.technic_name = cure.technic_name
    _cure.raw_material_price = cure.raw_material_price
    db.commit()
    db.refresh(_cure)
    return _cure


def update_cure_status(db: Session, cure: str, cure_id: uuid.UUID):
    _cure = get_cure_by_id(db, cure_id)
    _cure.is_done = cure
    _cure.updated_at = (datetime.datetime.now().isoformat(),)
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
    raw_material_price = 0
    for tooth in cure.payload_services:
        for services in tooth["services"]:
            service = db.query(Services).filter(Services.id == services).first()
            raw_material_price += service.raw_material_price
            _cure_service = OrtaCureService(
                service_id=services,
                tooth_id=tooth["id"],
                cure_id=_cure.id,
                service_name=service.name,
                service_price=service.price,
                raw_material_price=service.raw_material_price,
            )
            db.add(_cure_service)
    _cure.updated_at = datetime.datetime.now()
    _cure.price = cure.price
    _cure.raw_material_price = raw_material_price
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


def pay_with_technic_cure(db: Session, cure_id: uuid.UUID, cure: updateCure):
    _cure = get_cure_by_id(db, cure_id)
    _cure.updated_at = datetime.datetime.now()
    _cure.payed_raw_material_price += cure.price
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
