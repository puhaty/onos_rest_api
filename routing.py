from getters import Getters
from posts import post_flow


def dijkstra_algorithm(host_1, host_2, stream = 10):
    g = Getters()
    g.get_devices()
    g.get_links()
    g.get_hosts()
    q = g.devices.copy()
    s = set()
    devices = {}
    device_1 = set()
    device_2 = set()
    for device in q:
        devices[device.id] = device
    u = {}
    for host in g.hosts:
        if host_1 == host.ip_address:
            device_1 = host.device
        if host_2 == host.ip_address:
            device_2 = host.device
    for device in g.devices:
        u[device.id] = [999, 0]
    u[device_1.id] = [0, 0]
    u_copy = u.copy()
    while len(q) > 0:
        min_u = sorted(u_copy.items(), key=lambda x: x[1])  # (id,distance,previous)
        id = min_u[0][0]
        current_device = devices[id]
        q.remove(current_device)
        s.add(current_device)
        for link in current_device.links:
            if link.state == "ACTIVE":
                next_device = devices[link.dst.strip("of:")]
                if next_device in q:
                    d = u[next_device.id][0]
                    if d > (u[current_device.id][0] + link.value):
                        u[next_device.id][0] = (u[current_device.id][0] + link.value)
                        u[next_device.id][1] = current_device.id
        del u_copy[id]
    result = []

    def route(id):
        result.append(id)
        next_id = u[id][1]
        if next_id != 0:
            route(next_id)

    route(device_2.id)
    result.reverse()
    post_flow(host_1, host_2, result, stream)