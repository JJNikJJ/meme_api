from fastapi import FastAPI, UploadFile, File, HTTPException, status
from minio import Minio
from minio.error import S3Error
import os

app = FastAPI()

MINIO_URL = os.getenv("MINIO_URL", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadminsecret")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "memes")

minio_client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        minio_client.put_object(
            MINIO_BUCKET,
            file.filename,
            file.file,
            lenght=-1,
            part_size=10 * 1024 * 1024,
            content_type=file.content_type
        )
        return {"filename": file.filename}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
