import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.models import Tooth
from app.api.schemas import ToothSchema


def get_tooth(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tooth).offset(skip).limit(limit).all()


def get_tooth_by_id(db: Session, tooth_id: uuid.UUID):
    return db.query(Tooth).filter(Tooth.id == tooth_id).first()


def create_tooth(db: Session, tooth: ToothSchema):
    _tooth = Tooth(tooth_id=tooth.tooth_id, created_at=datetime.utcnow().isoformat())
    db.add(_tooth)
    db.commit()
    db.refresh(_tooth)
    return _tooth


def delete_tooth(db: Session, tooth_id: uuid.UUID):
    _tooth = get_tooth_by_id(db, tooth_id)
    db.delete(_tooth)
    db.commit()


def update_tooth(db: Session, tooth: ToothSchema):
    _tooth = get_tooth_by_id(db, tooth.id)
    _tooth.tooth_id = tooth.tooth_id
    _tooth.updated_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(_tooth)
    return _tooth
