import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.payments.crud import (
    get_payment,
    get_payment_by_id,
    create_payment,
    delete_payment,
    update_payment,
)
from app.api.schemas import Response, PaymentsSchema
from app.db import get_db

router = APIRouter()


@router.get("/{payment_id}")
async def get_payment_by_id_route(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    _payment = get_payment_by_id(db, payment_id)
    return Response(
        code=200, status="ok", message="success", result=_payment
    ).model_dump()


@router.get("/")
async def get_payment_route(
    skip: int | None = None,
    limit: int | None = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
):
    _payment = get_payment(db, skip, limit)
    return Response(
        code=200, status="ok", message="success", result=_payment
    ).model_dump()


@router.post("/")
async def create_payment_route(payment: PaymentsSchema, db: Session = Depends(get_db)):
    _payment = create_payment(db, payment)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{payment_id}")
async def delete_payment_route(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_payment(db, payment_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_payment_route(payment: PaymentsSchema, db: Session = Depends(get_db)):
    _payment = update_payment(db, payment)
    return Response(
        code=201, status="ok", message="updated", result=_payment
    ).model_dump()
