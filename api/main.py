from fastapi import FastAPI, UploadFile, File
import shutil
import os

from src.extract_ktp_data import extract_ktp_data

app = FastAPI()

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    return {"message": "API jalan"}


@app.post("/extract-ktp")
async def extract_ktp(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = extract_ktp_data(file_path)

    return result