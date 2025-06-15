import json, os, threading
from typing import Any

class StateManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.default_state = {
            "field1": "",
            "field1": "",
            "current_slide_show": {
                "timeout_default": 10,  # overwritten by "then_sleep" of each program
                "type": "slide_show",   # slide_show, constant
                "source": "all_uploaded_images",    # all_uploaded_images, programs_list
                "source_path": "local_data/uploaded_images",
                "current_file": "fileanme",
                "programs_list": [
                    {
                        "img_file": "fileanme",
                        "then_sleep": -1,
                    },
                    {
                        "img_file": "fileanme",
                        "then_sleep": -1,
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
        # current_state = self._read_state()
        # current_state.update(new_state)
        self._write_state(new_state)

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