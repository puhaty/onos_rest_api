import json_custom
from getters import Getters
from settings import session, http, headers, priority, timeout
    
def post_simple_flow(priority, timeout, deviceId, out_port, ip_dst):
    payload = json_custom.create_json(priority, timeout, deviceId, out_port, ip_dst)
    flow = session.post(f"{http}/flows/of:{deviceId}",
                        headers=headers,
                        json=payload)
    print(flow.status_code, " ", flow.reason)
    return flow

def delete_flows():
    for deviceId, id in g.flows.items():
        temp = session.delete(f"{http}/flows/of:{deviceId}/{id}")
        print(temp.status_code, " : ", temp.reason)


def delete_devices():
    for device_id in g.devices:
        temp = session.delete(f"{http}/devices/of:{device_id.id}")
        print(temp.status_code, " : ", temp.reason)

# delete_devices()
# delete_flows()
# post_simple_flow(40000, 0, "0000000000000001", "2", "10.0.0.2")
# post_simple_flow(40000, 0, "0000000000000001", "1", "10.0.0.1")
# post_simple_flow(40000, 0, "0000000000000002", "1", "10.0.0.2")
# post_simple_flow(40000, 0, "0000000000000002", "2", "10.0.0.1")
