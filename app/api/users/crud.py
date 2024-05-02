import datetime
import uuid
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.models import Users, Payments
from app.api.schemas import UserSchema


def get_user(
    db: Session, skip: int = 0, limit: int = 10, order_by: Optional[str] = None
):
    if skip < 0:
        skip = 0
    if order_by == "descend":
        return (
            db.query(Users).order_by(Users.name.desc()).offset(skip).limit(limit).all()
        )
    elif order_by == "ascend":
        return (
            db.query(Users).order_by(Users.name.asc()).offset(skip).limit(limit).all()
        )
    return (
        db.query(Users)
        .order_by(Users.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_users(db: Session):
    return db.query(func.count(Users.id)).scalar()


def qarz_user_count(db: Session):
    return db.query(Users).filter(Users.balance < 0).count()


def get_user_by_id(db: Session, user_id: uuid.UUID):
    return db.query(Users).filter(Users.id == user_id).first()


def create_user(db: Session, user: UserSchema):
    _user = Users(
        name=user.name,
        surname=user.surname,
        job=user.job,
        gender=user.gender,
        date_birth=user.date_birth,
        address=user.address,
        description=user.description,
        created_at=datetime.datetime.now().isoformat(),
        phone_number=user.phone_number,
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def delete_user(db: Session, user_id: uuid.UUID):
    db.query(Users).filter(Users.id == user_id).delete()
    db.query(Payments).filter(Payments.user_id == user_id).delete()
    db.commit()


def update_user(db: Session, user: UserSchema):
    _user = get_user_by_id(db=db, user_id=user.id)
    _user.name = user.name
    _user.surname = user.surname
    _user.job = user.job
    _user.date_birth = user.date_birth
    _user.address = user.address
    _user.updated_at = datetime.datetime.now().isoformat()
    _user.phone_number = user.phone_number
    db.commit()
    db.refresh(_user)
    return _user
