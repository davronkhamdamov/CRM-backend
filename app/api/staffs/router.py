import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.schemas import Response, StaffsSchema, UserImage, UserColor
from app.api.services.crud import get_service_by_id
from app.api.staffs.crud import (
    get_staff,
    get_staff_by_id,
    create_staff,
    delete_staff,
    update_staff,
    count_staffs,
    update_me,
    get_all_staffs,
    get_cures_for_salary,
    get_cure_services_for_salary,
    get_all_staff,
    update_staff_image,
    update_staff_color,
    get_cures_for_statistic,
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
    _count_of_staffs = count_staffs(
        db, current_user=current_user, search=req.query_params.get("search")
    )
    return Response(
        code=200,
        status="ok",
        message="success",
        result=_staffs,
        total=_count_of_staffs,
        info={"result": limit, "page": skip},
    ).model_dump()


@router.get("/all")
async def get_staffs_route(
    db: Session = Depends(get_db),
    _current_staff: dict = Depends(get_current_user),
):
    _staffs = get_all_staff(db)
    _count_of_staffs = count_staffs(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=_staffs,
        total=_count_of_staffs,
        current_staff=_current_staff,
    ).model_dump()


def date_components(date1):
    return date1.year, date1.month, date1.day


@router.get("/statistic")
async def get_staffs_salary_route(
    req: Request,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    month = req.query_params.get("month")
    cures_for_salary = get_cures_for_statistic(db=db, year_month=month)
    services_for_salary = get_cure_services_for_salary(db=db)

    _staffs = []
    if current_staff["role"] != "admin" and current_staff["role"] != "reception":
        _staffs = get_all_staff(db, staff_id=current_staff["id"])
    else:
        _staffs = get_all_staff(db)
    staffs = []
    for staff in _staffs:
        _staff = {
            "id": staff.id,
            "name": staff.name,
            "foiz": staff.foiz,
            "Maosh": 0,
        }
        if _staff not in staffs:
            staffs.append(_staff)
    for cure in cures_for_salary:
        for i, staff in enumerate(staffs):
            if cure.staff_id == staff["id"]:
                staffs[i]["Maosh"] += cure.price
                if cure.price == 0:
                    for service in services_for_salary:
                        if service.cure_id == cure.id:
                            staffs[i]["Maosh"] += int(
                                get_service_by_id(db, service.service_id).price
                            )

    _count_of_staffs = count_staffs(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=staffs,
        role=current_staff["role"],
    ).model_dump()


@router.get("/salary")
async def get_staffs_salary_route(
    req: Request,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    start_date = req.query_params.get("start-date")
    end_date = req.query_params.get("end-date")
    filter_staff = req.query_params.get("filter-staff")
    cures_for_salary = get_cures_for_salary(
        db=db,
        filter_staff=filter_staff,
        start_date_str=start_date,
        end_date_str=end_date,
    )
    services_for_salary = get_cure_services_for_salary(db=db)

    _staffs = get_all_staffs(db, skip, limit, staff_id=filter_staff)
    if current_staff["role"] != "admin" and current_staff["role"] != "reception":
        _staffs = get_all_staffs(db, skip, limit, staff_id=current_staff["id"])
    staffs = []
    for staff in _staffs:
        _staff = {
            "id": staff.id,
            "name": staff.name,
            "surname": staff.surname,
            "foiz": staff.foiz,
            "cures": [],
            "salary": 0,
        }

        if _staff not in staffs:
            staffs.append(_staff)
    for cure in cures_for_salary:
        for i, staff in enumerate(staffs):
            if cure.staff_id == staff["id"]:
                staffs[i]["cures"].append(cure)
                staffs[i]["salary"] += cure.price
                if cure.price == 0:
                    for service in services_for_salary:
                        if service.cure_id == cure.id:
                            staffs[i]["salary"] += int(
                                get_service_by_id(db, service.service_id).price
                            )

    _count_of_staffs = count_staffs(db)
    return Response(
        code=200,
        status="ok",
        message="success",
        result=staffs,
        role=current_staff["role"],
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


@router.put("/update-me")
async def update_staff_route(
    staff: StaffsSchema,
    db: Session = Depends(get_db),
    current_staff: dict = Depends(get_current_user),
):
    _staffs = update_me(db, staff, current_staff["id"])
    return Response(code=201, status="ok", message="updated").model_dump()


@router.put("/")
async def update_staff_route(
    staff: StaffsSchema,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = update_staff(db, staff)
    return Response(code=201, status="ok", message="updated").model_dump()


@router.put("/image/{staff_id}")
async def update_staff_route(
    staff_id: uuid.UUID,
    staff_image: UserImage,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = update_staff_image(db, staff_image.image_url, staff_id)
    return Response(code=201, status="ok", message="updated").model_dump()


@router.put("/color/{staff_id}")
async def update_staff_route(
    staff_id: uuid.UUID,
    staff_color: UserColor,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    _staffs = update_staff_color(db, staff_color.color, staff_id)
    return Response(code=201, status="ok", message="updated").model_dump()
