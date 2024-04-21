import uuid
from typing import Optional, List

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
)
from app.api.schemas import Response, CureSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user

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
            "end_time": cure.end_time,
            "staff_name": staff.name,
            "staff_surname": staff.surname,
            "created_at": cure.created_at,
        }
        for cure, staff, user in _cure
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
    payload_services: List[uuid.UUID],
    payload: List[int],
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    end_cure(db, cure_id, payload_services, payload)
    return Response(code=200, status="ok", message="updated").model_dump()
