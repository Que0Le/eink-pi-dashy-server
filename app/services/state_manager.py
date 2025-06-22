import json, os, threading
from typing import Any

from fastapi import Depends
from app.services.background_worker import BackgroundWorker


class StateManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.default_state = {
            "mode": "slide-show",  # or "static"

            "static_display": {
                "program": {
                "type": "image",         # e.g., "image", "weather", "calendar"
                "filename": "static.bmp" # or other relevant fields per program type
                }
            },

            "current_slide_show": {
                "name": "The first show",
                "device_name": "eink-pi-3",
                "display_name": "display-1-7.8-1872x1404",
                "loop": True,  # whether to loop the slideshow
                "timeout_default": 10,  # fallback sleep between slides if not overridden
                "programs_list": [
                {
                    "program": {
                    "type": "image",
                    "filename": "3.bmp"
                    },
                    "then_sleep": 10,
                    "repeat": 1
                },
                {
                    "program": {
                    "type": "image",
                    "filename": "2.bmp"
                    },
                    "then_sleep": 15,
                    "repeat": 2
                },
                {
                    "program": {
                    "type": "image",
                    "filename": "1.bmp"
                    },
                    "then_sleep": 20
                }
                ]
            }
        }


        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            self._write_state(self.default_state)

    def _read_state(self) -> dict:
        with self.lock:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

    def _write_state(self, data: dict):
        with self.lock:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    def get_state(self) -> dict:
        return self._read_state()

    def update_state(self, new_state: dict):
        """
        Update the state with a new state dictionary.
        """
        # from app.api.deps import get_background_worker  
        # worker: BackgroundWorker = get_background_worker()
        # current_state = self._read_state()
        # current_state.update(new_state)
        # print("New state submitted.")
        # print(json.dumps(new_state, indent=4, sort_keys=True))
        self._write_state(new_state)
        # Reload the programs

    def update_field(self, key: str, value: Any):
        state = self._read_state()
        state[key] = value
        self._write_state(state)

    def update_slide_show(self, slide_show: dict):
        state = self._read_state()
        state["current_slide_show"] = slide_show
        self._write_state(state)

    def append_program(self, program: dict):
        state = self._read_state()
        state["current_slide_show"]["programs_list"].append(program)
        self._write_state(state)

    def get_current_slideshow(self) -> dict:
        state = self._read_state()
        return state.get("current_slide_show", {})