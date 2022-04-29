from getters import Getters
from posts import post_flow


def Dijkstra_algorithm(host_1, host_2, stream=10) -> list():
    g = Getters()
    q = g.devices.copy()
    s = set()
    # Dict to help assigning nextSwitch based on link objects #
    devices = {}
    for device in q:
        devices[device.id] = device
    u = {}
    # checking src switch and dst switch #
    for host in g.hosts:
        if host_1 == host.ip:
            switch1 = host.switch
        if host_2 == host.ip:
            switch2 = host.switch
    for device in g.devices:
        u[device.id] = [999, 0]
    u[switch1.id] = [0, 0]  # distance, previous switch #
    u_copy = u.copy()
    while len(q) > 0:
        min_u = sorted(u_copy.items(), key=lambda x: x[1])  # (id,distance,previous)
        id = min_u[0][0]
        currentSwitch = devices[id]
        q.remove(currentSwitch)
        s.add(currentSwitch)
        for link in currentSwitch.links:
            if link.state == "ACTIVE":
                nextSwitch = devices[link.dst]
                if nextSwitch in q:
                    d = u[nextSwitch.id][0]
                    if d > (u[currentSwitch.id][0] + link.value):
                        u[nextSwitch.id][0] = (u[currentSwitch.id][0] + link.value)
                        u[nextSwitch.id][1] = currentSwitch.id
        del u_copy[id]
    # creating route list #
    result = []

    def route(id):
        result.append(id)
        next_id = u[id][1]
        if next_id != 0:
            route(next_id)

    route(switch2.id)
    result.reverse()
    post_flow(host_1, host_2, result, stream)