import time, os, shutil, subprocess

# Web server
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Drawing
# from lib import epd12in48b_V2
# from PIL import ImageDraw
# from PIL import ImageFont
# from PIL import ImageColor
# from PIL import Image

# Inititate
app = FastAPI()
# Allow React frontend on port 3000
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.178.98:3000",  # Include this if you're accessing via local IP
    "http://192.168.178.93",  # Include this if you're accessing via local IP
]

frontend_build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../ui-test/build"))
# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_dir, "static")), name="static")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html at root
@app.get("/")
def serve_root():
    return FileResponse(os.path.join(frontend_build_dir, "index.html"))
# Serve index.html for any unmatched route (for React Router)
@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    file_path = os.path.join(frontend_build_dir, full_path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_build_dir, "index.html"))

def display_imgs():
    time.sleep(2)
    executable_path = "./epd"
    if os.path.isfile(fname):
        print("clearing and go to sleep...")
        subprocess.run(["sudo", executable_path, "-v", "-1.39", "-m", "0", "-b", "./uploaded_images/image.png"], check=True)
        print("Task done.")
    else:
        print("No eink driver executable file at '" + executable_path + "'")

# POST endpoint to upload image
@app.post("/upload-pic")
async def upload_pic(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # print(f"Filename: {file.filename}, Content-type: {file.content_type}")
    # print(f"Size (via read): {len(contents)}")
    upload_folder = "uploaded_images"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    background_tasks.add_task(display_imgs)
    return {"filename": file.filename, "message": "Upload successful"}