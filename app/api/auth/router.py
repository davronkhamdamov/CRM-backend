import secrets
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth.crud import get_staff_from_by_login, validate_password
from app.api.models import Users
from app.api.schemas import LoginSchema, Response
from app.db import get_db
from app.utils.auth_middleware import create_access_token
from app.utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.initialize import store_otp, get_otp, delete_otp, get_otp_ttl
from app.utils.mail import send_email

router = APIRouter()


@router.post("/login")
async def login(staff: LoginSchema, db: Session = Depends(get_db)):
    _current_staff = get_staff_from_by_login(db=db, login=staff.login)
    if not _current_staff:
        raise HTTPException(status_code=401, detail="Bunday xodim topilmadi")
    check_password = validate_password(
        hashed_password=_current_staff.password, password=staff.password
    )
    if not check_password:
        raise HTTPException(status_code=400, detail="Parol notog'ri")
    return Response(
        code=200,
        status="ok",
        message="Successfully login",
        result={
            "role": _current_staff.role,
            "access_token": create_access_token(
                data={"id": str(_current_staff.id), "role": _current_staff.role},
                expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
            ),
        },
    ).model_dump()


@router.post("/generate-otp")
async def generate_otp(phone: str):
    otp = secrets.randbelow(1000000)
    otp_str = f"{otp:06}"
    expiration = datetime.now() + timedelta(minutes=5)
    await store_otp(phone, otp_str, int((expiration - datetime.now()).total_seconds()))

    subject = "Your OTP Code"
    body = f"""
    <html>
      <body>
        <h2>Sizning OTP kodingiz</h2>
        <p>OTP kodingiz: <strong>{otp_str}</strong></p>
        <p>OTP kodingiz 5 minutdan so'ng o'chib ketadi</p>
        <p>Eng yaxshi ezgu tilaklar bilan,<br>Cordial</p>
      </body>
    </html>
    """
    await send_email("davronx036@gmail.com", subject, body)
    return {"message": "OTP sent successfully"}


@router.post("/verify-otp")
async def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    stored_otp = await get_otp(phone)
    if not stored_otp:
        raise HTTPException(status_code=404, detail="No OTP found or OTP expired")

    if stored_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    await delete_otp(phone)
    subject = "Muvaffaqiyatli ro'yxatdan o'tdingiz 🎉"
    body = f"""
    <html>
      <body>
        <h2>Tabriklaymiz, siz ro'yxatdan o'tdingiz!</h2>
        <p>Sizning hisobingiz muvaffaqiyatli yaratilgan. Endi siz bizning xizmatlarimizdan foydalanishingiz mumkin.</p>
        <p>Agar hisobingizga kirishda yoki boshqa masalalarda yordamga ehtiyojingiz bo'lsa, biz bilan bog'laning.</p>
        <p>Yaxshi kunlar tilaymiz!</p>
        <p>Hurmat bilan,<br>Cordial</p>
      </body>
    </html>
    """
    _user = Users(phone_number=phone)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    await send_email("davronx036@gmail.com", subject, body)
    return Response(
        code=200,
        status="ok",
        message="Successfully registered",
        result={
            "access_token": create_access_token(
                data={"id": str(_user.id)},
                expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
            ),
        },
    ).model_dump()


@router.get("/otp-ttl")
async def check_otp_ttl(email: str):
    ttl = await get_otp_ttl(email)
    if ttl == "Key does not exist":
        raise HTTPException(status_code=404, detail="No OTP found")
    return {"email": email, "remaining_ttl": ttl}