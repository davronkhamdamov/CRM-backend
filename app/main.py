import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cure.router import router as cure_router
from app.api.payment_type.router import router as payment_type_router
from app.api.payments.router import router as payment_router
from app.api.services.router import router as service_router
from app.api.staffs.router import router as staffs_router
from app.api.tooth.router import router as tooth_router
from app.api.users.router import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_router, prefix="/user", tags=["Users"])
app.include_router(router=payment_router, prefix="/payment", tags=["Payments"])
app.include_router(
    router=payment_type_router, prefix="/payment-type", tags=["Payment type"]
)
app.include_router(router=tooth_router, prefix="/tooth", tags=["Tooth"])
app.include_router(router=cure_router, prefix="/cure", tags=["Cure"])
app.include_router(router=staffs_router, prefix="/staffs", tags=["Staffs"])
app.include_router(router=service_router, prefix="/service", tags=["Services"])

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
