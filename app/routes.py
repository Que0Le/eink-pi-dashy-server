from fastapi import APIRouter, HTTPException, Depends, Request
from app.dependencies import get_state_manager
from app.state_manager import StateManager
from app.dependencies import get_background_worker

router = APIRouter()

@router.get("/api/v1/start-task")
def start_task(worker = Depends(get_background_worker)):
    try:
        worker.start()
        return {"status": "Task started"}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/v1/stop-task")
def stop_task(worker = Depends(get_background_worker)):
    try:
        worker.stop()
        return {"status": "Task stopped"}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/v1/status")
def get_status(worker = Depends(get_background_worker)):
    return {"running": worker.is_running()}

@router.get("/api/v1/state")
def read_state(state: StateManager = Depends(get_state_manager)):
    return state.get_state()

@router.post("/api/v1/state")
async def set_state(request: Request, state: StateManager = Depends(get_state_manager)):
    """ TODO: apply new settings """
    data = await request.json()
    state.update_state(data)
    return {"message": "State updated", "data": data}