import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.schemas import Response, UserSchema
from app.api.users.crud import (
    get_user,
    get_user_by_id,
    create_user,
    delete_user,
    update_user,
)
from app.db import get_db

router = APIRouter()


@router.get("/{user_id}")
async def get_user_by_id_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    _users = get_user_by_id(db, user_id)
    return Response(code=200, status="ok", message="success", result=_users).dict()


@router.get("/")
async def get_users_route(
    skip: int | None = None,
    limit: int | None = Query(None, gt=9, lt=101),
    db: Session = Depends(get_db),
):
    _users = get_user(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_users).dict()


@router.post("/")
async def create_user_route(user: UserSchema, db: Session = Depends(get_db)):
    _users = create_user(db, user)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{user_id}")
async def delete_user_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return Response(code=200, status="ok", message="deleted").dict()


@router.put("/")
async def update_user_route(user: UserSchema, db: Session = Depends(get_db)):
    _user = update_user(db, user)
    return Response(code=200, status="ok", message="updated", result=_user).dict()
