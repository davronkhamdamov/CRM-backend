import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.models import Payment_type
from app.api.schemas import PaymentTypeSchema


def get_payment_type(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Payment_type).offset(skip).limit(limit).all()


def get_payment_type_by_id(db: Session, payment_type_id: uuid.UUID):
    return db.query(Payment_type).filter(Payment_type.id == payment_type_id).first()


def create_payment_type(db: Session, payment_type: PaymentTypeSchema):
    _payment_type = Payment_type(
        method=payment_type.method, created_at=datetime.now().isoformat()
    )
    db.add(_payment_type)
    db.commit()
    db.refresh(_payment_type)
    return _payment_type


def delete_payment_type(db: Session, payment_type_id: uuid.UUID):
    _payment_type = get_payment_type_by_id(db, payment_type_id)
    db.delete(_payment_type)
    db.commit()


def update_payment_type(db: Session, payment_type: PaymentTypeSchema):
    _payment_type = get_payment_type_by_id(db, payment_type.id)
    _payment_type.method = payment_type.method
    _payment_type.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_payment_type)
    return _payment_type
