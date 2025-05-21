```bash
# DO it once:
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install fastapi uvicorn pillow python-multipart

# activate environment
source .venv/bin/activate

# start web server
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# create an image with this page. Download black and red images
http://192.168.178.86:8000/static/ha/editpage.html
# upload pic to pi
http://192.168.178.86:8000/
# Now look at the console. Progress should be printed