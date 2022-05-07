class Device:
    def __init__(self, id, available):
        self.id = id
        self.available = available
        self.links = set()
        self.hosts = set()

    def __str__(self) -> str:
        device_str = "device:\n" + f"id : {self.id} available : {self.available} \nlinks: \n"
        for link in self.links:
            device_str += str(link) + "\n"
        device_str += f"host(s): {len(self.hosts)}\n"
        for host in self.hosts:
            device_str += str(host) + "\n"
        return device_str


class Host:
    def __init__(self, ip, mac, device, elem_id, port):
        self.ip_address = ip
        self.mac = mac
        self.device = device
        self.element_id = elem_id
        self.port = port

    def __str__(self) -> str:
        host_str = f"ip_address : {self.ip_address} mac_address : {self.mac} " \
                   + f"switch : {self.element_id} port : {self.port}"
        return host_str


class Link:
    def __init__(self, src, src_port, dst, dst_port, state, link_type, value=1):
        self.src = src
        self.src_port = src_port
        self.dst = dst
        self.dst_port = dst_port
        self.state = state
        self.link_type = link_type
        self.value = value

    def __str__(self) -> str:
        link_str = f"src : {self.src} port : {self.src_port} " \
                   + f"dst : {self.dst} dst_port : {self.dst_port} value : {self.value}"
        return link_str