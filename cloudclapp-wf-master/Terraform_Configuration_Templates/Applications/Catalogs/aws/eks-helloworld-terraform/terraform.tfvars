cluster_terraform_remote_state = ""

namespace = "my-app-ns"

message = "Hello World!"

backend_port      = 5000
backend_ifaddress = "0.0.0.0"
route             = "/my-app"

frontend_port = 80
node_port     = 30300

front_image = "nginx:1.7.9"
back_image  = "n1654/3-tier-app-python:0.1"

## backend image dockerfile
## >> FROM python:3
## >> RUN pip install --no-cache-dir --upgrade pip && \
## >>     pip install --no-cache-dir Flask
## >>
## >> CMD ["/home/main.py"]
