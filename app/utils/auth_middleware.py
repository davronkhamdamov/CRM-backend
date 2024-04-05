from datetime import timedelta, datetime

import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.utils.constants import SECRET_KEY, ALGORITHM

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        staff_id: str = payload.get("id")
        role: str = payload.get("role")
        if staff_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": staff_id, "role": role}
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    staff = decode_access_token(token)
    if not staff:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": staff["id"], "role": staff["role"]}
