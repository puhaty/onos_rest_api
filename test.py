import json
import requests
import json_custom

username = 'karaf'
password = 'karaf'
ip = "192.168.56.101"
port = "8181"
http = f"http://{ip}:{port}"
headers = {
    "Content-type": "application/json",
    "Accept": "application/json"
}

def post_flow(priority, timeout, deviceId, out_port, in_port, ip_dst):
    payload = json_custom.create_json(priority, timeout, deviceId, out_port, in_port, ip_dst)
    flow = requests.post(f"{http}/onos/v1/flows/of:{deviceId}",
                        auth = (username, password),
                        json = payload,
                        headers = headers)

    print(flow.status_code, " ", flow.reason)

post_flow(40000, 0, "0000000000000001", "3", "1", "10.0.0.4")
