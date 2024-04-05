import hashlib

from sqlalchemy.orm import Session

from app.api.models import Staffs


def get_staff_from_by_login(db: Session, login: str):
    return db.query(Staffs).filter(Staffs.login == login).first()


def validate_password(hashed_password: str, password: str):
    hashed_entered_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_entered_password == hashed_password
