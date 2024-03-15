import uvicorn
from fastapi import FastAPI

from api.router import router

app = FastAPI()

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
