import hashlib

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth.router import router as auth_route
from app.api.cure.router import router as cure_router
from app.api.models import Staffs
from app.api.payment_type.router import router as payment_type_router
from app.api.payments.router import router as payment_router
from app.api.services.router import router as service_router
from app.api.services_category.router import router as services_category
from app.api.staffs.router import router as staffs_router
from app.api.users.router import router as user_router
from app.db import db1

admin = db1.query(Staffs).filter(Staffs.login == "admin").first()

if not admin:
    _staff = Staffs(
        name="admin",
        surname="admin",
        address="Uzb",
        login="admin",
        password=hashlib.sha256("admin".encode()).hexdigest(),
        phone_number="+99898765432",
        gender="male",
        role="admin",
    )
    db1.add(_staff)
    db1.commit()

db1.close()

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_route, prefix="/auth", tags=["Login"])
app.include_router(router=user_router, prefix="/user", tags=["Users"])
app.include_router(router=payment_router, prefix="/payment", tags=["Payments"])
app.include_router(
    router=payment_type_router, prefix="/payment-type", tags=["Payment type"]
)
app.include_router(router=cure_router, prefix="/cure", tags=["Cure"])
app.include_router(router=staffs_router, prefix="/staffs", tags=["Staffs"])
app.include_router(router=service_router, prefix="/service", tags=["Services"])
app.include_router(
    router=services_category, prefix="/service-category", tags=["Services"]
)

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
