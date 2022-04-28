import requests

from settings import session, http
from components import Device, Host, Link


class Getters:
    def __init__(self):
        self.devices = set()
        self.hosts = set()
        self.links = set()

    def get_devices(self):
        try:
            url = f"{http}/devices"
            temp = session.get(url)
            # print(temp.status_code, " ", temp.reason)
            temp_json = temp.json()
            devices_temp = temp_json["devices"]
            for i in devices_temp:
                if (i["type"] == "SWITCH"):
                    self.devices.add(Device(i["id"].strip("of:"), i["available"]))
            for i in self.devices:
                print(i)
        except requests.HTTPError() as err:
            print(f"connection problem\n {err}")


    def get_hosts(self):
        host_device = 0
        try:
            url = f"{http}/hosts"
            temp = session.get(url)
            print(temp.status_code, " ", temp.reason)
            temp_json = temp.json()
            hosts_temp = temp_json["hosts"]
            print(hosts_temp)
            for i in hosts_temp:
                ip = i["ipAddresses"][0]
                mac = i["mac"]
                locations_dict = i["locations"][0]
                element_id = locations_dict["elementId"]
                port = locations_dict["port"]
            for i in self.devices:
                if i.id == element_id:
                    host_device = i
            host = Host(ip, mac, host_device, element_id, port)
            self.hosts.add(host)
            for i in self.devices:
                if i.id == host.element_id:
                    i.hosts.add(host)
            for i in self.hosts:
                print(i)
        except requests.HTTPError() as err:
            print(f"connection problem\n {err}")

    def get_links(self):
        try:
            url = f"{http}/links"
            temp = session.get(url)
            temp_json = temp.json()
            links_temp = temp_json["links"]
            for i in links_temp:
                src = i["src"]
                dst = i["dst"]
                state = i["state"]
                link_type = i["type"]
                for i in self.devices:
                    if i.id == src["device"]:
                        i.links.add(Link(src["device"], src["port"], dst["device"],\
                                         dst["port"], state, link_type))
                for i in self.devices:
                    print(i)
        except requests.HTTPError() as err:
            print(f"connection problem\n {err}")

g = Getters()
g.get_devices()
g.get_hosts()
g.get_links()

