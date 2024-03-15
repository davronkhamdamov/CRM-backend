import uuid

from fastapi import APIRouter, Depends
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


@router.get("/")
async def get_users_route(skip: int, limit: int, db: Session = Depends(get_db)):
    _users = get_user(db, skip, limit)
    return Response(code=200, status="ok", message="success", result=_users)


@router.get("/{user_id}")
async def get_user_by_id_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    _users = get_user_by_id(db, user_id)
    return Response(code=200, status="ok", message="success", result=_users)


@router.post("/")
async def create_user_route(user: UserSchema, db: Session = Depends(get_db)):
    _users = create_user(db, user)
    return Response(code=201, status="ok", message="created")


@router.delete("/{user_id}")
async def delete_user_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    _users = delete_user(db, user_id)
    return Response(code=200, status="ok", message="deleted")


@router.put("/{user_id}")
async def update_user_route(user: UserSchema, db: Session = Depends(get_db)):
    _users = update_user(db, user)
    return Response(code=200, status="ok", message="updated")
