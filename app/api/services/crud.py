import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.api.models import Services, ServicesCategory
from app.api.schemas import ServicesSchema


def get_service(
    db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None
):
    if skip < 0:
        skip = 0

    query = db.query(Services, ServicesCategory).join(
        Services, Services.service_category_id == ServicesCategory.id
    )
    if search:
        search = f"%{search}%"
        query = query.filter(Services.name.ilike(search))

    return query.offset(skip).limit(limit).all()


def get_service_by_id(db: Session, service_id: uuid.UUID):
    return db.query(Services).filter(Services.id == service_id).first()


def get_service_count(db: Session):
    return db.query(Services).filter(Services.status).count()


def create_service(db: Session, service: ServicesSchema):
    _service = Services(
        name=service.name,
        price=service.price,
        status=service.status,
        service_category_id=service.service_category_id,
        created_at=datetime.now().isoformat(),
    )
    db.add(_service)
    db.commit()
    db.refresh(_service)
    return _service


def delete_service(db: Session, service_id: uuid.UUID):
    _service = get_service_by_id(db, service_id)
    db.delete(_service)
    db.commit()


def update_service(db: Session, service: ServicesSchema, service_id: uuid.UUID):
    _service = get_service_by_id(db, service_id)
    _service.name = service.name
    _service.price = service.price
    _service.status = service.status
    _service.updated_at = datetime.now().isoformat()
    db.commit()
    db.refresh(_service)
    return _service
