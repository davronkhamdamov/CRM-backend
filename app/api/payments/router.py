import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.payments.crud import (
    get_payment,
    get_payment_by_id,
    create_payment,
    delete_payment,
    update_payment,
    count_payments,
)
from app.api.schemas import Response, PaymentsSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user
from app.utils.money_format import format_money

router = APIRouter()


@router.get("/{payment_id}")
async def get_payment_by_id_route(
    payment_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    _payment = get_payment_by_id(db, payment_id)
    return Response(
        code=200, status="ok", message="success", result=_payment
    ).model_dump()


@router.get("/")
async def get_payment_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1

    _payment = get_payment(
        db,
        skip,
        limit,
        search=req.query_params.get("search"),
    )
    count_of_payments = count_payments(db)
    results_dict = [
        {
            "amount": format_money(payment.amount),
            "payment_type_id": payment.payment_type_id,
            "method": payment_type.method,
            "username": user.name,
            "surname": user.surname,
            "id": payment.id,
            "user_id": user.id,
            "created_at": payment.created_at,
        }
        for payment, payment_type, user in _payment
    ]

    return Response(
        code=200,
        status="ok",
        message="success",
        result=results_dict,
        total=count_of_payments,
        info={"result": limit, "page": skip},
    ).model_dump()


@router.post("/")
async def create_payment_route(
    payment: PaymentsSchema, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    _payment = create_payment(db, payment)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{payment_id}")
async def delete_payment_route(
    payment_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    delete_payment(db, payment_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_payment_route(
    payment: PaymentsSchema, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    _payment = update_payment(db, payment)
    return Response(
        code=201, status="ok", message="updated", result=_payment
    ).model_dump()
