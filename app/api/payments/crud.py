import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Payments, Payment_type, Users
from app.api.schemas import PaymentsSchema
from app.api.users.crud import get_user_by_id


def get_payment(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    if skip < 0:
        skip = 0
    query = (
        db.query(Payments, Payment_type, Users)
        .select_from(Users)
        .join(Payments, Users.id == Payments.user_id)
        .join(Payment_type, Payments.payment_type_id == Payment_type.id)
    )
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Users.name.ilike(search), Users.surname.ilike(search)))

    return query.order_by(Payments.created_at.desc()).offset(skip).limit(limit).all()


def count_payments(db: Session):
    return db.query(func.count(Payments.id)).scalar()


def get_payment_by_id(db: Session, payment_id: uuid.UUID):
    return db.query(Payments).filter(Payments.id == payment_id).first()


def create_payment(db: Session, payment: PaymentsSchema):
    _payment = Payments(
        amount=payment.amount,
        payment_type_id=payment.payment_type_id,
        user_id=payment.user_id,
        created_at=datetime.now().isoformat(),
    )
    db.add(_payment)
    _user = get_user_by_id(db, user_id=payment.user_id)
    _user.balance += payment.amount
    db.commit()
    db.refresh(_payment)
    db.refresh(_user)
    return _payment


def delete_payment(db: Session, payment_id: uuid.UUID):
    _payment = get_payment_by_id(db, payment_id)
    db.delete(_payment)
    db.commit()


def update_payment(db: Session, payment: PaymentsSchema):
    _payment = get_payment_by_id(db, payment.id)
    _payment.payment_type_id = payment.payment_type_id
    _payment.user_id = payment.user_id
    _payment.updated_at = datetime.datetime.utcnow().isoformat()
    db.commit()
    db.refresh(_payment)
    return _payment
