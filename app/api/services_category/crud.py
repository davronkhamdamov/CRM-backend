import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.models import ServicesCategory
from app.api.schemas import ServicesCategorySchema


def get_service_category(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ServicesCategory).offset(skip).limit(limit).all()


def get_service_category_by_id(db: Session, service_id: uuid.UUID):
    return db.query(ServicesCategory).filter(ServicesCategory.id == service_id).first()


def create_service_category(db: Session, service: ServicesCategorySchema):
    _service = ServicesCategory(
        name=service.name,
        created_at=datetime.now().isoformat(),
    )
    db.add(_service)
    db.commit()
    db.refresh(_service)
    return _service


def delete_service_category(db: Session, service_id: uuid.UUID):
    _service = get_service_category_by_id(db, service_id)
    db.delete(_service)
    db.commit()


def update_service_category(db: Session, service: ServicesCategorySchema):
    _service = get_service_category_by_id(db, service.id)
    _service.name = service.name
    _service.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_service)
    return _service
