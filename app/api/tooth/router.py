import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import Response, ToothSchema
from app.api.tooth.crud import (
    get_tooth,
    get_tooth_by_id,
    create_tooth,
    delete_tooth,
    update_tooth,
)
from app.db import get_db

router = APIRouter()


@router.get("/")
async def get_tooth_route(skip: int, limit: int, db: Session = Depends(get_db)):
    _tooth = get_tooth(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_tooth)


@router.get("/{tooth_id}")
async def get_tooth_by_id_route(tooth_id: uuid.UUID, db: Session = Depends(get_db)):
    _tooth = get_tooth_by_id(db, tooth_id)
    return Response(code=200, status="ok", message="success", result=_tooth)


@router.post("/")
async def create_tooth_route(tooth: ToothSchema, db: Session = Depends(get_db)):
    create_tooth(db, tooth)
    return Response(code=201, status="ok", message="created")


@router.delete("/{tooth_id}")
async def delete_tooth_route(tooth_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_tooth(db, tooth_id)
    return Response(code=200, status="ok", message="deleted")


@router.put("/{tooth_id}")
async def update_tooth_route(tooth: ToothSchema, db: Session = Depends(get_db)):
    update_tooth(db, tooth)
    return Response(code=201, status="ok", message="updated")
