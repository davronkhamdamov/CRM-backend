import uuid

from fastapi import APIRouter, Depends
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


@router.get("/")
async def get_payment_type_route(skip: int, limit: int, db: Session = Depends(get_db)):
    _payment_type = get_payment_type(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_payment_type)


@router.get("/{payment_type_id}")
async def get_payment_type_by_id_route(
    payment_type_id: uuid.UUID, db: Session = Depends(get_db)
):
    _payment_type = get_payment_type_by_id(db, payment_type_id)
    return Response(code=200, status="ok", message="success", result=_payment_type)


@router.post("/")
async def create_payment_type_route(
    payment_type: PaymentTypeSchema, db: Session = Depends(get_db)
):
    _payment_type = create_payment_type(db, payment_type)
    return Response(code=201, status="ok", message="created")


@router.delete("/{payment_type_id}")
async def delete_payment_type_route(
    payment_type_id: uuid.UUID, db: Session = Depends(get_db)
):
    _payment_type = delete_payment_type(db, payment_type_id)
    return Response(code=200, status="ok", message="deleted")


@router.put("/{payment_type_id}")
async def update_payment_type_route(
    payment_type: PaymentTypeSchema, db: Session = Depends(get_db)
):
    _payment_type = update_payment_type(db, payment_type)
    return Response(code=200, status="ok", message="updated")
