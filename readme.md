```bash
# DO it once:
python3 -m venv .venv
source .venv/bin/activate
sudo apt install python3-pip
python3 -m pip install fastapi uvicorn python-multipart

# activate environment
source .venv/bin/activate

# start web server
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# create an image with this page. Download black and red images
http://192.168.178.86:8000/static/ha/editpage.html
# upload pic to pi
http://192.168.178.86:8000/
# Now look at the console. Progress should be printed

sudo ./epd -v -1.39 -m 0 -b "./pic/1872x1404_3.bmp"
```



```bash
sudo chown -R www-data:www-data eink-pi-web-ui/dist
sudo chmod -R o+rX eink-pi-web-ui/dist

sudo groupadd sharedrw
sudo usermod -aG sharedrw www-data
sudo usermod -aG sharedrw pi
sudo chown -R :sharedrw /data
sudo chmod -R 770 /data
```