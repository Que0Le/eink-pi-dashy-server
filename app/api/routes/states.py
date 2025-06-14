from app.core.config import settings

from app.services.background_worker import BackgroundWorker
from fastapi import APIRouter, HTTPException, Depends, Request
from app.api.deps import get_state_manager, get_background_worker
from app.state_manager import StateManager
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix="/states", tags=["states"])


@router.get("/start-task")
def start_task(worker=Depends(get_background_worker)):
    try:
        worker.start()
        return {"status": "Task started"}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stop-task")
def stop_task(worker: BackgroundWorker = Depends(get_background_worker)):
    try:
        worker.stop()
        return {"status": "Task stopped"}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status")
def get_status(worker: BackgroundWorker = Depends(get_background_worker)):
    return {"running": worker.is_running()}


@router.get("/state")
def read_state(state: StateManager = Depends(get_state_manager)):
    return state.get_state()


@router.post("/state")
async def set_state(request: Request, state: StateManager = Depends(get_state_manager)):
    """TODO: apply new settings"""
    data = await request.json()
    state.update_state(data)
    return {"message": "State updated", "data": data}


""""""


class ProgramEntry(BaseModel):
    filename: str
    then_sleep: int


class ProgramData(BaseModel):
    name: str
    device_name: str
    display_name: str
    programs_list: List[ProgramEntry]


@router.get("/current-slideshow")
def get_current_slideshow(state: StateManager = Depends(get_state_manager)):
    current_slideshow = state.get_current_slideshow()
    print(current_slideshow)
    return current_slideshow


@router.post("/current-slideshow", response_model=ProgramData)
def update_current_slideshow(
    program: ProgramData, state: StateManager = Depends(get_state_manager)
):
    print("Updated slideshow program: ", program)
    # TODO: store in state manager
    state.update_slide_show(program.dict())
    print(state.get_current_slideshow())
    return program
