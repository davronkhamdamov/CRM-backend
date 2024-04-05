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

router = APIRouter()


@router.get("/")
async def get_staffs_route(req: Request, db: Session = Depends(get_db)):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 0) - 1
    _staffs = get_staff(db=db, skip=skip, limit=limit)
    _count_of_staffs = count_staffs(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=_staffs,
        total=_count_of_staffs,
        info={"result": limit, "page": skip},
    ).model_dump()


@router.get("/{staff_id}")
async def get_staff_by_id_route(staff_id: uuid.UUID, db: Session = Depends(get_db)):
    _staffs = get_staff_by_id(db, staff_id)
    return Response(
        code=200, status="ok", message="success", result=_staffs
    ).model_dump()


@router.post("/")
async def create_staff_route(staff: StaffsSchema, db: Session = Depends(get_db)):
    _staffs = create_staff(db, staff)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{staff_id}")
async def delete_staff_route(staff_id: uuid.UUID, db: Session = Depends(get_db)):
    _staffs = delete_staff(db, staff_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_staff_route(staff: StaffsSchema, db: Session = Depends(get_db)):
    _staffs = update_staff(db, staff)
    return Response(code=201, status="ok", message="updated").model_dump()
