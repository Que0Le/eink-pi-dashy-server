import time, os, shutil, subprocess, logging, sys

def display_img(filepath: str):
    time.sleep(2)
    executable_path = "./epd"
    if os.path.isfile(executable_path):
        print("clearing and go to sleep...")
        subprocess.run(["sudo", executable_path, "-v", "-1.39", "-m", "0", "-b", filepath], check=True)
        print("Task done.")
    else:
        print("No eink driver executable file at '" + executable_path + "'")