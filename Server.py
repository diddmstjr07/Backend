from fastapi import FastAPI
from router.user import user
from router.reservation import reservation
from router.garbage_can import garbage_can
from router.photo import photo
from router.garbage import garbage
from router.spring_flower import flower
from router.livestreaming import stream
import uvicorn
import router.util.sql_es as q
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
app.include_router(flower)
app.include_router(stream)

@app.get("/")
async def root():
    return {"Server_page"}

if __name__ == "__main__":
    uvicorn.run("Server:app", host='0.0.0.0', port=8000, reload=True)