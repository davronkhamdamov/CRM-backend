import datetime
import uuid

from sqlalchemy.orm import Session

from app.api.models import Services
from app.api.schemas import ServicesSchema


def get_service(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Services).offset(skip).limit(limit).all()


def get_service_by_id(db: Session, service_id: uuid.UUID):
    return db.query(Services).filter(Services.id == service_id)


def create_service(db: Session, service: ServicesSchema):
    _service = Services(service)
    db.add(_service)
    db.commit()
    db.refresh(_service)
    return _service


def delete_service(db: Session, service_id: uuid.UUID):
    _service = get_service_by_id(service_id)
    db.delete(_service)
    db.commit()


def update_service(db: Session, service: ServicesSchema):
    _service = get_service_by_id(service.id)
    _service.name = service.name
    _service.price = service.price
    _service.raw_material_price = service.raw_material_price
    _service.service_price_price = service.service_price_price
    _service.updated_at = datetime.UTC
    db.commit()
    db.refresh(_service)
