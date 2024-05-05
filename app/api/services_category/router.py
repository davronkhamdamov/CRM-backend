import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, ServicesCategorySchema
from app.api.services_category.crud import (
    get_service_category,
    get_service_category_by_id,
    create_service_category,
    delete_service_category,
    update_service_category,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/")
async def get_services_category_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _services = get_service_category(db, skip, limit)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": service.id,
                "name": service.name,
                "created_at": service.created_at,
                "updated_at": service.updated_at,
            }
            for service in _services
        ],
    ).model_dump()


@router.get("/{service_category_id}")
async def get_service_category_by_id_route(
    service_category_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _services = get_service_category_by_id(db, service_category_id)
    return Response(
        code=200, status="ok", message="success", result=_services
    ).model_dump()


@router.post("/")
async def create_service_category_route(
    service_category: ServicesCategorySchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _service = create_service_category(db, service_category)
    return Response(
        code=201, status="ok", message="created", result=_service
    ).model_dump()


@router.delete("/{service_category_id}")
async def delete_service_route(
    service_category_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_service_category(db, service_category_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_service_route(
    service_category: ServicesCategorySchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _service = update_service_category(db, service_category)
    return Response(
        code=201, status="ok", message="updated", result=_service
    ).model_dump()
