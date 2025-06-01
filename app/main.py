import time, os, shutil, subprocess, logging, sys
from pathlib import Path

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from app.dependencies import init_state_manager, init_background_worker
from app.display import display_imgs

UPLOAD_FOLDER = "local_data/uploaded_images"
CONFIG_FOLDER = "local_data/"

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_state_manager(CONFIG_FOLDER + "/state.json")
    init_background_worker()
app.include_router(router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.178.98:3000",  # Include this if you're accessing via local IP
    "http://192.168.178.93",  # Include this if you're accessing via local IP
]


app.mount("/api/v1/all-images/", StaticFiles(directory=UPLOAD_FOLDER), name="All Images")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/images")
def all_images():
    return [f.name for f in Path(UPLOAD_FOLDER).iterdir() if f.is_file()]

# POST endpoint to upload image
@app.post("/api/v1/upload-pic")
async def upload_pic(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # print(f"Filename: {file.filename}, Content-type: {file.content_type}")
    # print(f"Size (via read): {len(contents)}")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "Upload successful"}

@app.post("/api/v1/upload-and-display-img")
async def upload_and_display_img(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    background_tasks.add_task(display_imgs, file_path=file_path)
    return {"filename": file.filename, "message": "Upload successful. Added to queue."}