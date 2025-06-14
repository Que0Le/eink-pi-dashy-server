import time, os, shutil, subprocess, logging, sys
from pathlib import Path

from app.api.main import api_router
from app.core.config import settings

# logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn").setLevel(logging.INFO)  # override uvicorn logs
logging.getLogger("app").setLevel(logging.DEBUG)  # your app logs

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# from .routes import router
# from app.dependencies import init_state_manager, init_background_worker
# from app.services.display import display_img

# UPLOAD_FOLDER = "local_data/uploaded_images"
# CONFIG_FOLDER = "local_data/"

# app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.178.98:3000",  # Include this if you're accessing via local IP
    "http://192.168.178.93",  # Include this if you're accessing via local IP
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if not os.path.isdir(settings.UPLOAD_FOLDER):
    try:
        Path(settings.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)
        exit(1)

app.mount(
    "/api/v1/all-images/",
    StaticFiles(directory=settings.UPLOAD_FOLDER),
    name="All Images",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# @app.on_event("startup")
# def startup_event():
#     init_state_manager(settings.CONFIG_FOLDER + "/state.json")
#     init_background_worker()
# app.include_router(router)


# @app.get("/api/v1/images")
# def all_images():
#     return [f.name for f in Path(UPLOAD_FOLDER).iterdir() if f.is_file()]

# @app.delete("/api/v1/images/{filename}")
# def delete_image(filename: str):
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     if not os.path.exists(file_path):
#         return {"error": "File not found"}, 404
#     try:
#         os.remove(file_path)
#         return {"message": "File deleted successfully"}
#     except Exception as e:
#         logging.error(f"Error deleting file {filename}: {e}")
#         return {"error": "Failed to delete file"}, 500

# @app.get("/api/v1/display-image/{filename}")
# def display_image(background_tasks: BackgroundTasks, filename: str):
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     if not os.path.exists(filepath):
#         return {"error": "File not found"}, 404
#     try:
#         background_tasks.add_task(display_img, filepath=filepath)
#         # display_img(file_path)
#         return {"message": f"Displaying image {filename} in background"}
#     except Exception as e:
#         logging.error(f"Error displaying image {filename}: {e}")
#         return {"error": "Failed to display image"}, 500

# # POST endpoint to upload image
# @app.post("/api/v1/upload-img")
# async def upload_pic(file: UploadFile = File(...)):
#     # print(f"Filename: {file.filename}, Content-type: {file.content_type}")
#     # print(f"Size (via read): {len(contents)}")
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"filename": file.filename, "message": "Upload successful"}

# @app.post("/api/v1/upload-and-display-img")
# async def upload_and_display_img(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     background_tasks.add_task(display_img, filepath=filepath)
#     return {"filename": file.filename, "message": "Upload successful. Added to queue."}
