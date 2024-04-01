import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, UserSchema
from app.api.users.crud import (
    get_user,
    get_user_by_id,
    create_user,
    delete_user,
    update_user,
    count_users,
)
from app.db import get_db

router = APIRouter()


@router.get("/{user_id}")
async def get_user_by_id_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    _users = get_user_by_id(db, user_id)
    return Response(
        code=200, status="ok", message="success", result=_users
    ).model_dump()


@router.get("/")
async def get_users_route(
    req: Request,
    db: Session = Depends(get_db),
):

    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 0) - 1
    _users = get_user(
        db, limit=limit, skip=skip, order_by=req.query_params.get("order")
    )
    _count_of_users = count_users(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=_users,
        total=_count_of_users,
        info={"result": limit, "page": skip},
    ).dict()


@router.post("/")
async def create_user_route(user: UserSchema, db: Session = Depends(get_db)):
    create_user(db, user)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{user_id}")
async def delete_user_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()


@router.put("/")
async def update_user_route(user: UserSchema, db: Session = Depends(get_db)):
    _user = update_user(db, user)
    return Response(code=200, status="ok", message="updated", result=_user).model_dump()
