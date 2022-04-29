import requests

from settings import session, http
from components import Device, Host, Link


class Getters:
    def __init__(self):
        self.devices = set()
        self.hosts = set()
        self.get_links()
        self.get_hosts()
        self.get_devices()

    def get_devices(self):
        try:
            url = f"{http}/devices"
            temp = session.get(url)
            temp_json = temp.json()
            devices_temp = temp_json["devices"]
            for device in devices_temp:
                if (device["type"] == "SWITCH"):
                    self.devices.add(Device(device["id"].strip("of:"), device["available"]))
        except requests.HTTPError() as err:
            print(f"connection problem\n {err}")

    def get_links(self):
        try:
            url = f"{http}/links"
            temp = session.get(url)
            temp_json = temp.json()
            links_temp = temp_json["links"]
            for link in links_temp:
                src = link["src"]
                dst = link["dst"]
                state = link["state"]
                link_type = link["type"]
                for device in self.devices:
                    if device.id == src["device"].strip("of:"):
                        device.links.add(Link(src["device"], src["port"], dst["device"],\
                                         dst["port"], state, link_type))
        except requests.HTTPError() as err:
            print(f"connection problem\n {err}")

    def get_hosts(self):
        host_device = 0
        try:
            url = f"{http}/hosts"
            temp = session.get(url)
            temp_json = temp.json()
            hosts_temp = temp_json["hosts"]
            for host in hosts_temp:
                ip = host["ipAddresses"][0]
                mac = host["mac"]
                locations_dict = host["locations"][0]
                element_id = locations_dict["elementId"]
                port = locations_dict["port"]
                for device in self.devices:
                    if device.id == element_id.strip("of:"):
                        host_device = device
                host = Host(ip, mac, host_device, element_id.strip(":of"), port)
                self.hosts.add(host)
                for device in self.devices:
                    if device.id == host.element_id:
                        device.hosts.add(host)
        except requests.HTTPError() as err:
            print(f"connection problem\n {err}")

    def print_devices(self):
        for device in self.devices:
            print(device)

# g = Getters()
# g.get_devices()
# g.get_links()
# g.get_hosts()
# g.print_devices()

