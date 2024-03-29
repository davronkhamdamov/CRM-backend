import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.models import Payments
from app.api.schemas import PaymentsSchema


def get_payment(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Payments).offset(skip).limit(limit).all()


def get_payment_by_id(db: Session, payment_id: uuid.UUID):
    return db.query(Payments).filter(Payments.id == payment_id).first()


def create_payment(db: Session, payment: PaymentsSchema):
    _payment = Payments(
        amount=payment.amount,
        payment_type_id=payment.payment_type_id,
        user_id=payment.user_id,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(_payment)
    db.commit()
    db.refresh(_payment)
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
