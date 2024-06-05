import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, UserSchema, Prikus, UserImage
from app.api.users.crud import (
    get_user,
    get_user_by_id,
    create_user,
    delete_user,
    update_user,
    count_users,
    qarz_user_count,
    update_user_prikus,
    update_user_image,
)
from app.db import get_db
from app.utils.auth_middleware import get_current_user

router = APIRouter()


@router.get("/count")
async def get_user_by_id_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _users = count_users(db)
    return Response(
        code=200, status="ok", message="success", result=_users
    ).model_dump()


@router.get("/qarz-count")
async def get_user_by_id_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _users = qarz_user_count(db)
    return Response(
        code=200, status="ok", message="success", result=_users
    ).model_dump()


@router.get("/statistic_by_address")
async def get_user_by_id_route(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _users = get_user(db)
    address_users = {}
    for user in _users:
        if user.address in address_users:
            address_users[user.address] += 1
        else:
            address_users[user.address] = 1
    return Response(
        code=200, status="ok", message="success", result=address_users
    ).model_dump()


@router.get("/{user_id}")
async def get_user_by_id_route(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _user = get_user_by_id(db, user_id)
    return Response(code=200, status="ok", message="success", result=_user).model_dump()


@router.get("/")
async def get_users_route(
    req: Request,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    debt = req.query_params.get("debt")
    _users = get_user(
        db,
        limit=limit,
        skip=skip,
        order_by=req.query_params.get("order"),
        search=req.query_params.get("search"),
        debt=debt,
    )
    _count_of_users = []
    if debt == "true":
        _count_of_users = qarz_user_count(db)
    else:
        _count_of_users = count_users(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=[
            {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "date_birth": user.date_birth,
                "address": user.address,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "job": user.job,
                "description": user.description,
                "balance": user.balance,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in _users
        ],
        total=_count_of_users,
        info={"result": limit, "page": skip},
    ).dict()


@router.post("/")
async def create_user_route(
    user: UserSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    create_user(db, user)
    return Response(code=201, status="ok", message="created").dict()


@router.delete("/{user_id}")
async def delete_user_route(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    delete_user(db, user_id)
    return Response(
        code=200,
        status="ok",
        message="deleted",
    ).model_dump()


@router.put("/{user_id}")
async def update_user_route(
    user_id: uuid.UUID,
    user: UserSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _user = update_user(db, user, user_id)
    return Response(code=200, status="ok", message="updated", result=_user).model_dump()


@router.put("/image/{user_id}")
async def update_user_route(
    user_id: uuid.UUID,
    user_image: UserImage,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _user = update_user_image(db, user_image.image_url, user_id)
    return Response(code=200, status="ok", message="updated", result=_user).model_dump()


@router.put("/prikus/{user_id}")
async def update_user_route(
    user_id: uuid.UUID,
    prikus: Prikus,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _user = update_user_prikus(db, prikus.prikus, user_id)
    return Response(code=200, status="ok", message="updated", result=_user).model_dump()
