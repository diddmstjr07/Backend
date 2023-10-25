from fastapi import UploadFile # fastip를 호출하는 모듈
from fastapi import APIRouter
import os
import uuid

photo = APIRouter(prefix='/photo')

@photo.post("/get", tags=['photo'])
async def upload_photo(file: UploadFile):
    UPLOAD_DIR = "/var/www/html/photo"

    content = await file.read()
    filename = f"{str(uuid.uuid4())}.jpg"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)
        
    return {"filename": filename}
