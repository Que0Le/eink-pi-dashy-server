```bash
# DO it once:
python3 -m venv .venv
source .venv/bin/activate
sudo apt install python3-pip
python3 -m pip install fastapi uvicorn python-multipart

# activate environment
cd eink-pi-dashy-server/
source .venv/bin/activate

# start web server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug


# create an image with this page. Download black and red images
http://192.168.178.86:8000/static/ha/editpage.html
# upload pic to pi
http://192.168.178.86:8000/
# Now look at the console. Progress should be printed

# docs
http://192.168.178.57:8000/docs


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

```
sudo cat /etc/nginx/sites-enabled/default 
server {
    listen 80;
    client_max_body_size 50M;
#    server_name _;  # or use _ for default
#    location / {
#    	root /data/;
#    }

    # Serve static files for /webui from /path/webui
    #location /webui/ {
    #    alias /data/eink-pi-web-ui/dist/; 
    #    index index.html;
    #    try_files $uri $uri/ /index.html;
    #}
    location / {
	    proxy_pass http://localhost:9000/;
	    proxy_set_header Host $host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	    proxy_set_header X-Forwarded-Proto $scheme;
	}
    # Optional: Redirect plain /webui to /webui/
    #location = /webui {
    #    return 301 /webui/;
    #}

    # Proxy API requests to FastAPI backend
    location /api/v1/ {
        proxy_pass http://localhost:8000/api/v1/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```