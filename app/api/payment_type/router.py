import uuid

from fastapi import APIRouter, Depends, Query
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

router = APIRouter()


@router.get("/{payment_type_id}")
async def get_payment_type_by_id_route(
    payment_type_id: uuid.UUID, db: Session = Depends(get_db)
):
    _payment_type = get_payment_type_by_id(db, payment_type_id)
    return Response(code=200, status="ok", message="success", result=_payment_type)


@router.get("/")
async def get_payment_type_route(
    skip: int | None = None,
    limit: int | None = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
):
    _payment_type = get_payment_type(db, skip, limit)
    return Response(
        code=200, status="ok", message="success", result=_payment_type
    ).dict()


@router.post("/")
async def create_payment_type_route(
    payment_type: PaymentTypeSchema, db: Session = Depends(get_db)
):
    _payment_type = create_payment_type(db, payment_type)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{payment_type_id}")
async def delete_payment_type_route(
    payment_type_id: uuid.UUID, db: Session = Depends(get_db)
):
    delete_payment_type(db, payment_type_id)
    return Response(code=200, status="ok", message="deleted").dict()


@router.put("/")
async def update_payment_type_route(
    payment_type: PaymentTypeSchema, db: Session = Depends(get_db)
):
    _payment_type = update_payment_type(db, payment_type)
    return Response(
        code=200, status="ok", message="updated", result=payment_type
    ).dict()
