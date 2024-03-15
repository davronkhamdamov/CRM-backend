import datetime
import uuid

from sqlalchemy.orm import Session

from app.api.models import Cure
from app.api.schemas import CureSchema


def get_cures(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cure).offset(skip).limit(limit).all()


def get_cure_by_id(db: Session, user_id: uuid.UUID):
    return db.query(Cure).filter(Cure.id == user_id)


def create_cure(db: Session, cure: CureSchema):
    _cure = Cure(cure)
    db.add(_cure)
    db.commit()
    db.refresh(_cure)
    return _cure


def delete_cure(db: Session, cure_id: uuid.UUID):
    _cure = get_cure_by_id(cure_id)
    db.delete(_cure)
    db.commit()


def update_cure(db: Session, cure: CureSchema):
    _cure = get_cure_by_id(cure.id)
    _cure.name = cure.name
    _cure.surname = cure.surname
    _cure.job = cure.job
    _cure.date_birth = cure.date_birth
    _cure.address = cure.address
    _cure.updated_at = datetime.UTC
    _cure.phone_number = cure.phone_number
    db.commit()
    db.refresh(_cure)
