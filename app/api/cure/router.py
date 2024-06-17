import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Request
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
    update_cure_status,
    get_cures_for_staff_count,
    get_debt_cures,
    get_cures_count,
    get_cures_for_schedule,
)
from app.api.schemas import Response, CureSchema, updateCure, PaymentsSchema, Status
from app.api.staffs.router import date_components
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/for-staff")
async def get_cures_for_staff_route(
    req: Request,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    start_date = req.query_params.get("start-date")
    end_date = req.query_params.get("end-date")
    filters = {"pay": [], "status": []}
    for key in req.query_params:
        if key.startswith("filters[5]"):
            filters["pay"].append(req.query_params.getlist(key)[0])
        elif key.startswith("filters[is_done]"):
            filters["status"].append(req.query_params.getlist(key)[0])
    _cure = get_cures_for_staff(
        db, current_staff["id"], start_date, end_date, skip, limit, filters
    )
    _cure_count = get_cures_for_staff_count(db, current_staff["id"], filters)
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
        code=200, status="ok", message="success", result=result_dict, total=_cure_count
    ).model_dump()


@router.get("/for-staff/{staff_id}")
async def get_cures_for_staff_route(
    req: Request,
    db: Session = Depends(get_db),
    staff_id: uuid.UUID = None,
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1

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
    req: Request,
    db: Session = Depends(get_db),
    patient_id: uuid.UUID = None,
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
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
    result_dict = []
    for _cure_service, _service in _cure:
        if _cure_service.service_name and _cure_service.service_price:
            result_dict.append(
                {
                    "cure_id": _cure_service.id,
                    "service_name": _cure_service.service_name,
                    "tooth_id": _cure_service.tooth_id,
                    "price": _cure_service.service_price,
                    "created_at": _cure_service.created_at,
                }
            )
        else:
            result_dict.append(
                {
                    "cure_id": _cure_service.id,
                    "service_name": _service.name,
                    "tooth_id": _cure_service.tooth_id,
                    "price": _service.price,
                    "created_at": _cure_service.created_at,
                }
            )

    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/debt")
async def get_cures_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    staff = req.query_params.get("filter-staff")
    _cure = get_debt_cures(db, staff)
    result_dict = []
    start_time = req.query_params.get("start-date")
    end_time = req.query_params.get("end-date")
    for cure, staff, user in _cure:
        if start_time != "null" and end_time != "null":
            iso_start_datetime = datetime.fromisoformat(
                start_time.replace("Z", "+00:00")
            )
            iso_end_datetime = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            if (
                date_components(iso_start_datetime)
                <= date_components(cure.start_time)
                <= date_components(iso_end_datetime)
            ):
                result_dict.append(
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
                )
        else:
            result_dict.append(
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
            )
    return Response(
        code=200,
        status="ok",
        message="success",
        result=result_dict,
        total=len(result_dict),
    ).model_dump()


@router.get("/for-schedule")
async def get_cures_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    staff = req.query_params.get("filter-staff")
    _cure = get_cures_for_schedule(db, staff)
    result_dict = []
    for cure, staff, user in _cure:
        result_dict.append(
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
        )
    return Response(
        code=200,
        status="ok",
        message="success",
        result=result_dict,
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
        "prikus": _cure[1].prikus,
        "disease_progression": _cure[1].disease_progression,
        "objective_check": _cure[1].objective_check,
        "milk": _cure[1].milk,
        "placental_diseases": _cure[1].placental_diseases,
        "staff_name": _cure[2].name,
        "staff_surname": _cure[2].surname,
        "created_at": _cure[0].created_at,
    }

    return Response(
        code=200, status="ok", message="success", result=result_dict
    ).model_dump()


@router.get("/")
async def get_cures_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    staff = req.query_params.get("filter-staff")
    start_time = req.query_params.get("start-date")
    end_time = req.query_params.get("end-date")
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    filters = {"pay": [], "status": []}
    for key in req.query_params:
        if key.startswith("filters[5]"):
            filters["pay"].append(req.query_params.getlist(key)[0])
        elif key.startswith("filters[is_done]"):
            filters["status"].append(req.query_params.getlist(key)[0])

    _cure = get_cures(db, staff, start_time, end_time, filters, skip, limit)
    _cure_count = get_cures_count(db, staff, start_time, end_time, filters)
    result_dict = []
    for cure, staff, user in _cure:
        result_dict.append(
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
        )
    return Response(
        code=200,
        status="ok",
        message="success",
        result=result_dict,
        total=_cure_count,
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


@router.put("/status/{cure_id}")
async def update_cure_route(
    cure_id: uuid.UUID,
    cure: Status,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    update_cure_status(db, cure.status, cure_id)
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
