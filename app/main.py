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
# if settings.all_cors_origins:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=settings.all_cors_origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

