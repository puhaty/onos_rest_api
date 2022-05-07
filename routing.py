from getters import Getters
from posts import post_simple_flow
from settings import session, http, headers, priority, timeout

class Routing:
    def __init__(self):
        self.g = Getters()
        self.g.get_devices()
        self.g.get_links()
        self.g.get_hosts()
        self.g.get_flows()

    def post_flow(self, host_1, host_2, route, stream):
        devices = {}
        for device in self.g.devices:
            devices[device.id] = device
        print("The shortest path: ",route)
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
                        link.value += stream
            elif current_device.id == route[-1]:
                for host in current_device.hosts:
                    if host.ip_address == host_2:
                        post_simple_flow(priority, timeout, device_id, host.port, host_2)
                for link in current_device.links:
                    index = route.index(device_id)
                    if link.dst == route[index - 1]:
                        post_simple_flow(priority, timeout, device_id, link.src_port, host_1)
                        link.value += stream
            else:
                for link in current_device.links:
                    index = route.index(device_id)
                    if link.dst == route[index - 1]:
                        post_simple_flow(priority, timeout, device_id, link.src_port, host_1)
                    elif link.dst == route[index + 1]:
                        post_simple_flow(priority, timeout, device_id, link.src_port, host_2)
                        link.value += stream
    
    def the_shorthest_path(self, host_1, host_2, stream = 10):
        q = self.g.devices.copy()
        s = set()
        devices = {}
        device_1 = set()
        device_2 = set()
        for device in q:
            devices[device.id] = device
        u = {}
        for host in self.g.hosts:
            if host_1 == host.ip_address:
                device_1 = host.device
            if host_2 == host.ip_address:
                device_2 = host.device
        for device in self.g.devices:
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
        self.post_flow(host_1, host_2, result, stream)