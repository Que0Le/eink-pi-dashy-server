from app.state_manager import StateManager
from app.services.background_worker import BackgroundWorker

# Singleton instance of the state manager
state_manager_instance: StateManager | None = None
background_worker_instance: BackgroundWorker | None = None

def init_state_manager(file_path: str):
    global state_manager_instance
    state_manager_instance = StateManager(file_path)

def get_state_manager() -> StateManager:
    assert state_manager_instance is not None, "StateManager not initialized"
    return state_manager_instance

def init_background_worker():
    global background_worker_instance
    background_worker_instance = BackgroundWorker(interval=20)

def get_background_worker() -> BackgroundWorker:
    assert background_worker_instance is not None
    return background_worker_instance
