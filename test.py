import json
import requests

username = 'karaf'
password = 'karaf'
http = 'http://192.168.56.101:8181'
filename = r'C:\Users\PuHaty\Documents\python\scht_restapi\flows\switch1.json'
headers = {
    'Content-type': 'application/json',
    "Accept": "application/json"
}
with open(filename, "r") as file:
    default_payload = json.load(file)

#def create_json()

xd = requests.post(http + "/onos/v1/flows/of:0000000000000001",
                   auth = (username, password),
                   json = default_payload,
                   headers = headers)

print(xd.status_code, " ", xd.reason)
