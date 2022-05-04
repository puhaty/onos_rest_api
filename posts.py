import json_custom
from getters import Getters
from settings import session, http, headers, priority, timeout

g = Getters()
g.get_devices()
g.get_links()
g.get_hosts()
g.get_flows()


def post_simple_flow(priority, timeout, deviceId, out_port, ip_dst):
    payload = json_custom.create_json(priority, timeout, deviceId, out_port, ip_dst)
    flow = session.post(f"{http}/flows/of:{deviceId}",
                        headers=headers,
                        json=payload)
    print(flow.status_code, " ", flow.reason)
    return flow


def xd():
    devices = {}
    for device in g.devices:
        devices[device.id] = device


def post_flow(host_1, host_2, route, stream):
    devices = {}
    for device in g.devices:
        devices[device.id] = device
    print(route)
    for device_id in route:
        current_device = devices[device_id]
        if current_device.id == route[0]:
            for host in current_device.hosts:
                if host.ip_address == host_1:
                    post_simple_flow(priority, timeout, device_id, host.port, host_1)
            for link in current_device.links:
                index = route.index(device_id)
                if link.dst == route[index + 1]:
                    post_simple_flow(priority, timeout, device_id, link.src_port, host_2)
        elif current_device.id == route[-1]:
            for host in current_device.hosts:
                if host.ip_address == host_2:
                    post_simple_flow(priority, timeout, device_id, host.port, host_2)
            for link in current_device.links:
                index = route.index(device_id)
                if link.dst == route[index - 1]:
                    post_simple_flow(priority, timeout, device_id, link.src_port, host_1)
        else:
            for link in current_device.links:
                index = route.index(device_id)
                if link.dst == route[index - 1]:
                    post_simple_flow(priority, timeout, device_id, link.src_port, host_1)
                elif link.dst == route[index + 1]:
                    post_simple_flow(priority, timeout, device_id, link.src_port, host_2)

def delete_flows():
    for deviceId, id in g.flows.items():
        session.delete(f"{http}/flows/of:{deviceId}/{id}")


delete_flows()
# post_simple_flow(40000, 0, "0000000000000001", "2", "10.0.0.2")
# post_simple_flow(40000, 0, "0000000000000001", "1", "10.0.0.1")
# post_simple_flow(40000, 0, "0000000000000002", "1", "10.0.0.2")
# post_simple_flow(40000, 0, "0000000000000002", "2", "10.0.0.1")
# xd()
