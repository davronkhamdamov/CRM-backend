import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.schemas import Response, ServicesSchema
from app.api.services.crud import (
    get_service,
    get_service_by_id,
    create_service,
    delete_service,
    update_service,
)
from app.db import get_db

router = APIRouter()


@router.get("/")
async def get_services_route(
    skip: int | None = None,
    limit: int | None = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
):
    _services = get_service(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_services).model_dump()


@router.get("/{service_id}")
async def get_service_by_id_route(service_id: uuid.UUID, db: Session = Depends(get_db)):
    _services = get_service_by_id(db, service_id)
    return Response(code=200, status="ok", message="success", result=_services).model_dump()


@router.post("/")
async def create_service_route(service: ServicesSchema, db: Session = Depends(get_db)):
    _service = create_service(db, service)
    return Response(code=201, status="ok", message="created", result=_service).model_dump()


@router.delete("/{service_id}")
async def delete_service_route(service_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_service(db, service_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_service_route(service: ServicesSchema, db: Session = Depends(get_db)):
    _service = update_service(db, service)
    return Response(code=201, status="ok", message="updated", result=_service).model_dump()
