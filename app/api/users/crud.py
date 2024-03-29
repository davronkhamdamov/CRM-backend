import datetime
import uuid

from sqlalchemy.orm import Session

from app.api.models import Users
from app.api.schemas import UserSchema


def get_user(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Users).offset(skip).limit(limit).all()


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
        created_at=datetime.datetime.utcnow().isoformat(),
        phone_number=user.phone_number,
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def delete_user(db: Session, user_id: uuid.UUID):
    _user = get_user_by_id(db, user_id)
    db.delete(_user)
    db.commit()


def update_user(db: Session, user: UserSchema):
    _user = get_user_by_id(db=db, user_id=user.id)
    _user.name = user.name
    _user.surname = user.surname
    _user.job = user.job
    _user.date_birth = user.date_birth
    _user.address = user.address
    _user.updated_at = datetime.datetime.utcnow().isoformat()
    _user.phone_number = user.phone_number
    db.commit()
    db.refresh(_user)
    return _user
