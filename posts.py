import json_custom
from getters import Getters
from settings import session, http, headers

def post_simple_flow(priority, timeout, deviceId, out_port, ip_dst):
    payload = json_custom.create_json(priority, timeout, deviceId, out_port, ip_dst)
    flow = session.post(f"{http}/flows/of:{deviceId}",
                        headers = headers,
                        json = payload)
    return flow
    # print(flow.status_code, " ", flow.reason)

def post_flow(host_1, host_2, route, stream):
    devices = {}
    g = Getters()
    for device in g.devices:
        devices[device.id] = device
    for device_id in route:
        current_device = devices[device.id]
        if current_device.id == route[0]:
            for host in current_device.hosts:
                if host.ip == host_1:
                    post_simple_flow(40000, 40, device_id, host.ip_address, host.port)
                    break
            for link in current_device.links:
                index = route.index(device_id)
                if link.dst == route[index + 1]:
                    post_simple_flow(40000, 40, device_id, host_2, link.src_port)
                    link.value = + int(stream)
        elif current_device.id == route[-1]:
            for host in current_device.hosts:
                if host.ip == host_2:
                    post_simple_flow(40000, 40, device_id, host.ip_address, host.port)
                    break
            for link in current_device.links:
                index = route.index(device_id)
                if link.dst == route[index - 1]:
                    post_simple_flow(40000, 40, device_id, host_1, link.src_port)
                    link.value = + int(stream)
        else:
            for link in current_device.links:
                index = route.index(device_id)
                if link.dst == route[index - 1]:
                    post_simple_flow(40000, 40, device_id, host_1, link.src_port)
                elif link.dst == route[index + 1]:
                    post_simple_flow(40000, 40, device_id, host_2, link.src_port)
                    link.value = + int(stream)


post_simple_flow(40000, 0, "0000000000000001", "3", "10.0.0.4")