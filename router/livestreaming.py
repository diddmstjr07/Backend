from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import base64

stream = APIRouter(prefix='/stream')

class Frame(BaseModel):
    frame: str


@stream.post("/get", tags=['stream'])
async def get_frame(stream: Frame):
    global frame_bytes
    frame_bytes = base64.b64decode(stream.frame)

@stream.get("/show", tags=['stream'])
def show_frame():
    def frame_stream():
        while True:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(frame_bytes) + b'\r\n')
        
    return StreamingResponse(frame_stream(), media_type="multipart/x-mixed-replace; boundary=frame")