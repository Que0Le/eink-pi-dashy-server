import uuid, os, shutil, logging
from typing import Any
from pathlib import Path
from app.core.config import settings

from fastapi import APIRouter, FastAPI, File, UploadFile, BackgroundTasks
from app.services.display import display_img

# from app.api.deps import CurrentUser, SessionDep
# from app.models import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate, Message

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/images")
def all_images():
    return [f.name for f in Path(settings.UPLOAD_FOLDER).iterdir() if f.is_file()]


@router.delete("/images/{filename}")
def delete_image(filename: str):
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404
    try:
        os.remove(file_path)
        return {"message": "File deleted successfully"}
    except Exception as e:
        logging.error(f"Error deleting file {filename}: {e}")
        return {"error": "Failed to delete file"}, 500


@router.get("/display-image/{filename}")
def display_image(background_tasks: BackgroundTasks, filename: str):
    filepath = os.path.join(settings.UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}, 404
    try:
        background_tasks.add_task(display_img, filepath=filepath)
        # display_img(file_path)
        return {"message": f"Displaying image {filename} in background"}
    except Exception as e:
        logging.error(f"Error displaying image {filename}: {e}")
        return {"error": "Failed to display image"}, 500


# POST endpoint to upload image
@router.post("/upload-img")
async def upload_pic(file: UploadFile = File(...)):
    # print(f"Filename: {file.filename}, Content-type: {file.content_type}")
    # print(f"Size (via read): {len(contents)}")
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(str(settings.UPLOAD_FOLDER), str(file.filename))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "Upload successful"}


@router.post("/upload-and-display-img")
async def upload_and_display_img(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(str(settings.UPLOAD_FOLDER), str(file.filename))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    background_tasks.add_task(display_img, filepath=file_path)
    return {"filename": file.filename, "message": "Upload successful. Added to queue."}
