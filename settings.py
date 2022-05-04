import json
import requests
import json_custom

username = 'karaf'
password = 'karaf'
ip = "192.168.56.101"
port = "8181"
http = f"http://{ip}:{port}/onos/v1"
headers = {
    "Content-type": "application/json",
    "Accept": "application/json"
}
priority = 40000
timeout = 40
session = requests.session()
session.auth = (username, password)
