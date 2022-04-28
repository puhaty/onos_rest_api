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
session = requests.session()
session.auth = (username, password)


def post_simple_flow(priority, timeout, deviceId, out_port, in_port, ip_dst):
    payload = json_custom.create_json(priority, timeout, deviceId, out_port, in_port, ip_dst)
    flow = session.post(f"{http}/flows/of:{deviceId}",
                        headers = headers,
                        json = payload)
    print(flow.status_code, " ", flow.reason)



#post_simple_flow(40000, 0, "0000000000000001", "3", "1", "10.0.0.4")
