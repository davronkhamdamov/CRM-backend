import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.cure.crud import get_cures_by_user_id
from app.api.payments.crud import get_payment_by_user_id
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
    get_users,
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


@router.get("/cure")
async def get_cures_route(
        req: Request,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    start_time = req.query_params.get("start-date")
    end_time = req.query_params.get("end-date")
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    filters = {"pay": [], "status": []}
    for key in req.query_params:
        if key.startswith("filters[5]"):
            filters["pay"].append(req.query_params.getlist(key)[0])
        elif key.startswith("filters[is_done]"):
            filters["status"].append(req.query_params.getlist(key)[0])

    _cure, _cure_count = get_cures_by_user_id(db, current_user['id'], start_time, end_time, filters, skip, limit)
    result_dict = []
    for cure, staff, user in _cure:
        result_dict.append(
            {
                "cure_id": cure.id,
                "user_id": user.id,
                "is_done": cure.is_done,
                "start_time": cure.start_time,
                "end_time": cure.end_time,
                "price": cure.price,
                "payed_price": cure.payed_price,
                "staff_name": staff.name,
                "staff_surname": staff.surname,
                "created_at": cure.created_at,
            }
        )
    return Response(
        code=200,
        status="ok",
        message="success",
        result=result_dict,
        total=_cure_count,
    ).model_dump()


@router.get("/payment")
async def get_payment_by_id_route(
        req: Request,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    start_date = req.query_params.get("start-date")
    end_date = req.query_params.get("end-date")

    _payments, total = get_payment_by_user_id(
        db,
        current_user['id'],
        page=skip,
        per_page=limit,
        start_date_str=start_date,
        end_date_str=end_date
    )
    return Response(
        code=200, status="ok", message="success", result=_payments, totoal=total
    ).model_dump()


@router.get("/get-me")
async def get_user_by_id_route(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    _user = get_user_by_id(db, current_user["id"])
    return Response(
        code=200, status="ok", message="success", result=_user
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
    _users = get_users(db)
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
    ).model_dump()


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


@router.put("/image")
async def update_staff_route(
        staff_image: UserImage,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    update_user_image(db, staff_image.image_url, current_user['id'])
    return Response(code=201, status="ok", message="updated").model_dump()


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
