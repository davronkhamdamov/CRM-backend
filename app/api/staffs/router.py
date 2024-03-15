import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import Response, StaffsSchema
from app.api.staffs.crud import (
    get_staff,
    get_staff_by_id,
    create_staff,
    delete_staff,
    update_staff,
)
from app.db import get_db

router = APIRouter()


@router.get("/")
async def get_staffs_route(skip: int, limit: int, db: Session = Depends(get_db)):
    _staffs = get_staff(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_staffs)


@router.get("/{staff_id}")
async def get_staff_by_id_route(staff_id: uuid.UUID, db: Session = Depends(get_db)):
    _staffs = get_staff_by_id(db, staff_id)
    return Response(code=200, status="ok", message="success", result=_staffs)


@router.post("/")
async def create_staff_route(staff: StaffsSchema, db: Session = Depends(get_db)):
    _staffs = create_staff(db, staff)
    return Response(code=201, status="ok", message="created")


@router.delete("/{staff_id}")
async def delete_staff_route(staff_id: uuid.UUID, db: Session = Depends(get_db)):
    _staffs = delete_staff(db, staff_id)
    return Response(code=200, status="ok", message="deleted")


@router.put("/{staff_id}")
async def update_staff_route(staff: StaffsSchema, db: Session = Depends(get_db)):
    _staffs = update_staff(db, staff)
    return Response(code=201, status="ok", message="updated")
