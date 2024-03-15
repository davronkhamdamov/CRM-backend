import uvicorn
from fastapi import FastAPI

from app.api.users.router import router

app = FastAPI()

app.include_router(router=router, prefix="/user", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
