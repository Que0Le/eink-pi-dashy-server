import threading, time
from pathlib import Path

from app.display import display_img

UPLOAD_FOLDER = "local_data/uploaded_images"

class BackgroundWorker:
    def __init__(self, interval: int = 5):
        self.interval = interval
        self.thread = None
        self.stop_event = threading.Event()

    def _task(self):
        while not self.stop_event.is_set():
            from app.dependencies import get_state_manager
            print("[Worker] Doing periodic work...")
            state = get_state_manager()
            curr_state = state.get_state()
            if curr_state.get("current_slide_show").get("type") == "slide_show":
                all_files = [f.name for f in Path(UPLOAD_FOLDER).iterdir() if f.is_file()]
                current_file = curr_state.get("current_slide_show").get("current_file")
                # get the "next" item in a circular list:
                try:
                    index = all_files.index(current_file)
                    next_file = all_files[(index + 1) % len(all_files)]
                except ValueError:
                    print("[Worker] Current file not found in the list, resetting to first file.")
                    next_file = all_files[0] if all_files else None
                #
                file_path = Path(UPLOAD_FOLDER) / next_file
                print(f"[Worker] Displaying image: {file_path}")
                display_img(file_path)
                #
                print("Save current file to state")
                curr_state["current_slide_show"]["current_file"] = next_file
                state.update_state(curr_state)
            else:
                print("[Worker] No image to display.")
            time.sleep(self.interval)
        print("[Worker] Gracefully stopped.")

    def start(self):
        if self.thread and self.thread.is_alive():
            raise RuntimeError("Worker already running.")
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._task, daemon=True)
        self.thread.start()

    def stop(self):
        if not self.thread or not self.thread.is_alive():
            raise RuntimeError("Worker is not running.")
        self.stop_event.set()
        self.thread.join()

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()
