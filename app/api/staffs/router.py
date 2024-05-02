import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, StaffsSchema
from app.api.staffs.crud import (
    get_staff,
    get_staff_by_id,
    create_staff,
    delete_staff,
    update_staff,
    count_staffs,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/")
async def get_staffs_route(
    req: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    _staffs = get_staff(
        db=db,
        skip=skip,
        limit=limit,
        current_user=current_user,
        search=req.query_params.get("search"),
        order_by=req.query_params.get("order"),
    )
    _count_of_staffs = count_staffs(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=_staffs,
        total=_count_of_staffs,
        info={"result": limit, "page": skip},
    ).model_dump()


@router.get("/get-me")
async def get_me(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _staff = get_staff_by_id(db, current_user["id"])
    return Response(
        code=200, status="ok", message="success", result=_staff
    ).model_dump()


@router.get("/count")
async def get_me(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _count_of_staffs = count_staffs(db)
    return Response(
        code=200, status="ok", message="success", result=_count_of_staffs
    ).model_dump()


@router.get("/{staff_id}")
async def get_staff_by_id_route(
    staff_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = get_staff_by_id(db, staff_id)
    return Response(
        code=200, status="ok", message="success", result=_staffs
    ).model_dump()


@router.post("/")
async def create_staff_route(
    staff: StaffsSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = create_staff(db, staff)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{staff_id}")
async def delete_staff_route(
    staff_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = delete_staff(db, staff_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_staff_route(
    staff: StaffsSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = update_staff(db, staff)
    return Response(code=201, status="ok", message="updated").model_dump()
