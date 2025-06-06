import time, os, shutil, subprocess, logging, sys

# Web server
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

background_thread = None
stop_event = Event()

# Inititate
app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# StreamHandler für die Konsole
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d]"
    "\n[%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.debug("Starting FastAPI server...")
logger.info("FastAPI server started successfully.")


# Worker function
def background_task():
    while not stop_event.is_set():
        print("Doing some background work...")
        time.sleep(5)  # Wake up every 5 seconds
    print("Background task stopping gracefully.")

# Allow React frontend on port 3000
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.178.98:3000",  # Include this if you're accessing via local IP
    "http://192.168.178.93",  # Include this if you're accessing via local IP
]

UPLOAD_FOLDER = "uploaded_images"

app.mount("/api/v1/all-images/", StaticFiles(directory=UPLOAD_FOLDER), name="All Images")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def display_imgs(file_path: str):
    time.sleep(2)
    executable_path = "./epd"
    if os.path.isfile(executable_path):
        print("clearing and go to sleep...")
        subprocess.run(["sudo", executable_path, "-v", "-1.39", "-m", "0", "-b", file_path], check=True)
        print("Task done.")
    else:
        print("No eink driver executable file at '" + executable_path + "'")

@app.get("/api/v1/images")
def all_images():
    print("he")
    return ["image.png", "2025_05_24T21_51_11_711Z__49949168_326750594598992_3929980949416116224_n_jpg_1872x1404.bmp"]

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