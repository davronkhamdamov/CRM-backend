import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, ServicesSchema
from app.api.services.crud import (
    get_service,
    get_service_by_id,
    create_service,
    delete_service,
    update_service,
    get_service_count,
    get_service_for_category,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user
from app.utils.money_format import format_money

router = APIRouter()


@router.get("/by-category")
async def get_services_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _services = get_service_for_category(db)
    result = []
    for _, category in _services:
        _category = {
            "id": category.id,
            "name": category.name,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
            "services": [],
        }

        if _category not in result:
            result.append(_category)

    for _service, _ in _services:
        for i, e in enumerate(result):
            if e["id"] == _service.service_category_id:
                result[i]["services"].append(_service)

    return Response(
        code=200,
        status="ok",
        message="success",
        result=result,
    ).model_dump()


@router.get("/")
async def get_services_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _services = get_service(
        db,
        skip,
        limit,
        search=req.query_params.get("search"),
    )
    _count_of_services = get_service_count(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": service.id,
                "name": service.name,
                "price": format_money(service.price),
                "category_id": services_category.id,
                "category_name": services_category.name,
                "status": service.status,
                "created_at": service.created_at,
                "updated_at": service.updated_at,
            }
            for service, services_category in _services
        ],
        total=_count_of_services,
        info={"result": limit, "page": skip},
    ).model_dump()


@router.get("/count")
async def get_service_by_id_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _services_count = get_service_count(db)
    return Response(
        code=200, status="ok", message="success", result=_services_count
    ).model_dump()


@router.get("/{service_id}")
async def get_service_by_id_route(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _services = get_service_by_id(db, service_id)
    _services.price = format_money(_services.price)
    return Response(
        code=200, status="ok", message="success", result=_services
    ).model_dump()


@router.post("/")
async def create_service_route(
    service: ServicesSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _service = create_service(db, service)
    return Response(
        code=201, status="ok", message="created", result=_service
    ).model_dump()


@router.delete("/{service_id}")
async def delete_service_route(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_service(db, service_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/{service_id}")
async def update_service_route(
    service: ServicesSchema,
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _service = update_service(db, service, service_id)
    return Response(
        code=201, status="ok", message="updated", result=_service
    ).model_dump()
