import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.cure.crud import (
    create_cure,
    get_cures,
    get_cure_by_id,
    update_cure,
    delete_cure,
)
from app.api.schemas import Response, CureSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/{cure_id}")
async def get_cure_by_id_route(
    cure_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    _cure = get_cure_by_id(db, cure_id)
    return Response(code=200, status="ok", message="success", result=_cure).model_dump()


@router.get("/")
async def get_cures_route(
    skip: int | None = None,
    limit: int | None = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    _cure = get_cures(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_cure).model_dump()


@router.post("/")
async def create_cure_route(
    user: CureSchema,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    _cure = create_cure(db, user)
    return Response(code=201, status="ok", message="created").model_dump()


@router.delete("/{cure_id}")
async def delete_cure_route(
    cure_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    delete_cure(db, cure_id)
    return Response(code=200, status="ok", message="deleted").model_dump()


@router.put("/")
async def update_cure_route(
    cure: CureSchema,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    update_cure(db, cure)
    return Response(code=200, status="ok", message="updated").model_dump()
