import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.payment_type.crud import (
    get_payment_type,
    get_payment_type_by_id,
    create_payment_type,
    delete_payment_type,
    update_payment_type,
)
from app.api.schemas import Response, PaymentTypeSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/{payment_type_id}")
async def get_payment_type_by_id_route(
    payment_type_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _payment_type = get_payment_type_by_id(db, payment_type_id)
    return Response(
        code=200, status="ok", message="success", result=_payment_type
    ).model_dump()


@router.get("/")
async def get_payment_type_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _payment_type = get_payment_type(db, skip, limit)
    return Response(
        code=200, status="ok", message="success", result=_payment_type
    ).model_dump()


@router.post("/")
async def create_payment_type_route(
    payment_type: PaymentTypeSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_payment_type(db, payment_type)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{payment_type_id}")
async def delete_payment_type_route(
    payment_type_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_payment_type(db, payment_type_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_payment_type_route(
    payment_type: PaymentTypeSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _payment_type = update_payment_type(db, payment_type)
    return Response(
        code=200, status="ok", message="updated", result=payment_type
    ).model_dump()
