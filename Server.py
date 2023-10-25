from fastapi import FastAPI # fastip를 호출하는 모듈
from router.user import user
from router.reservation import reservation
from router.garbage_can import garbage_can
from router.photo import photo
from router.garbage import garbage
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #fastip 모듈을 변수에 저장~

app.add_middleware(
    CORSMiddleware,
    allow_origins= "*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(reservation)
app.include_router(photo)
app.include_router(garbage_can)
app.include_router(garbage)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main":
    uvicorn.run("Server:app", host='0.0.0.0', reload=True)