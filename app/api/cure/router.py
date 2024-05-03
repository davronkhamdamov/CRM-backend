import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.cure.crud import (
    create_cure,
    get_cures,
    update_cure,
    delete_cure,
    get_cure_by_id_for_staff,
    get_cures_for_staff,
    end_cure,
    get_cure_with_service,
    pay_with_balance_cure,
    pay_with_cash_cure,
    get_cures_for_patient,
    get_cures_for_staff_by_id,
)
from app.api.schemas import Response, CureSchema, updateCure, PaymentsSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user
from app.utils.money_format import format_money

router = APIRouter()


@router.get("/for-staff")
async def get_cures_for_staff_route(
    skip: Optional[int] = None,
    limit: Optional[int] = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    _cure = get_cures_for_staff(db, current_staff["id"], skip, limit)
    result_dict = [
        {
            "cure_id": cure.id,
            "user_id": user.id,
            "user_name": user.name,
            "user_surname": user.surname,
            "is_done": cure.is_done,
            "start_time": cure.start_time,
            "price": cure.price,
            "payed_price": cure.payed_price,
            "end_time": cure.end_time,
            "staff_name": staff.name,
            "description": user.description,
            "staff_surname": staff.surname,
            "created_at": cure.created_at,
        }
        for cure, staff, user in _cure
    ]
    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/for-staff/{staff_id}")
async def get_cures_for_staff_route(
    skip: Optional[int] = None,
    limit: Optional[int] = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
    staff_id: uuid.UUID = None,
    _=Depends(get_current_user),
):
    _cure = get_cures_for_staff_by_id(db, staff_id, skip, limit)
    result_dict = [
        {
            "cure_id": cure.id,
            "user_id": user.id,
            "user_name": user.name,
            "user_surname": user.surname,
            "is_done": cure.is_done,
            "start_time": cure.start_time,
            "price": cure.price,
            "payed_price": cure.payed_price,
            "end_time": cure.end_time,
            "staff_name": staff.name,
            "description": user.description,
            "staff_surname": staff.surname,
            "created_at": cure.created_at,
        }
        for cure, staff, user in _cure
    ]
    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/for-patient/{patient_id}")
async def get_cures_for_staff_route(
    skip: Optional[int] = None,
    limit: Optional[int] = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
    patient_id: uuid.UUID = None,
    _=Depends(get_current_user),
):
    _cure = get_cures_for_patient(db, patient_id, skip, limit)
    result_dict = [
        {
            "cure_id": cure.id,
            "user_id": user.id,
            "user_name": user.name,
            "user_surname": user.surname,
            "is_done": cure.is_done,
            "start_time": cure.start_time,
            "price": cure.price,
            "payed_price": cure.payed_price,
            "end_time": cure.end_time,
            "staff_name": staff.name,
            "description": user.description,
            "staff_surname": staff.surname,
            "created_at": cure.created_at,
        }
        for cure, staff, user in _cure
    ]
    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/cure-service/{cure_id}")
async def get_cure_service(
    cure_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _cure = get_cure_with_service(db, cure_id)
    result_dict = [
        {
            "cure_id": _cure_service.id,
            "service_name": _service.name,
            "tooth_id": _cure_service.tooth_id,
            "price": format_money(_service.price),
            "created_at": _cure_service.created_at,
        }
        for _cure_service, _service in _cure
    ]
    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/{cure_id}")
async def get_cure_by_id_route(
    cure_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    _cure = get_cure_by_id_for_staff(db, cure_id, current_staff["id"])
    result_dict = {
        "cure_id": _cure[0].id,
        "user_id": _cure[1].id,
        "user_name": _cure[1].name,
        "user_surname": _cure[1].surname,
        "is_done": _cure[0].is_done,
        "start_time": _cure[0].start_time,
        "end_time": _cure[0].end_time,
        "price": _cure[0].price,
        "payed_price": _cure[0].payed_price,
        "description": _cure[1].description,
        "staff_name": _cure[2].name,
        "staff_surname": _cure[2].surname,
        "created_at": _cure[0].created_at,
    }

    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/")
async def get_cures_route(
    skip: Optional[int] = None,
    limit: Optional[int] = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _cure = get_cures(db, skip, limit)
    result_dict = [
        {
            "cure_id": cure.id,
            "user_id": user.id,
            "user_name": user.name,
            "user_surname": user.surname,
            "is_done": cure.is_done,
            "start_time": cure.start_time,
            "end_time": cure.end_time,
            "price": cure.price,
            "payed_price": cure.payed_price,
            "staff_name": staff.name,
            "staff_surname": staff.surname,
            "created_at": cure.created_at,
        }
        for cure, staff, user in _cure
    ]
    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.post("/")
async def create_cure_route(
    cure: CureSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _cure = create_cure(db, cure)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{cure_id}")
async def delete_cure_route(
    cure_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_cure(db, cure_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_cure_route(
    cure: CureSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    update_cure(db, cure)
    return Response(code=200, status="ok", message="updated").model_dump()


@router.put("/update/{cure_id}")
async def update_cure_route(
    cure_id: uuid.UUID,
    cure: updateCure,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    end_cure(
        db=db,
        cure_id=cure_id,
        cure=cure,
        is_done=cure.is_done,
    )
    return Response(code=200, status="ok", message="updated").model_dump()


@router.put("/pay-balance/{cure_id}")
async def update_cure_route(
    cure_id: uuid.UUID,
    cure: updateCure,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    pay_with_balance_cure(db=db, cure_id=cure_id, cure=cure)
    return Response(code=200, status="ok", message="updated").model_dump()


@router.put("/pay/{cure_id}")
async def update_cure_route(
    cure_id: uuid.UUID,
    payment: PaymentsSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    pay_with_cash_cure(db=db, cure_id=cure_id, payment=payment)
    return Response(code=200, status="ok", message="updated").model_dump()
