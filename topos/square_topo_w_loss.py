from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo(Topo):

    def build(self):

        # Add hosts and switches:
        left_up_Host = self.addHost('h1')
        right_up_Host = self.addHost('h2')
        left_down_Host = self.addHost('h3')
        right_down_Host = self.addHost('h4')
        left_up_Switch = self.addSwitch('s1')
        right_up_Switch = self.addSwitch('s2')
        left_down_Switch = self.addSwitch('s3')
        right_down_Switch = self.addSwitch('s4')

        # Add links:
        self.addLink(left_up_Host, left_up_Switch)
        self.addLink(right_up_Host, right_up_Switch)
        self.addLink(left_down_Host, left_down_Switch)
        self.addLink(right_down_Host, right_down_Switch)
        self.addLink(left_up_Switch, right_up_Switch, cls=TCLink, bw=10, delay='30ms')
        self.addLink(left_up_Switch, left_down_Switch, cls = TCLink, bw = 10, delay = '30ms')
        self.addLink(right_up_Switch, right_down_Switch, cls = TCLink, bw = 10, delay = '30ms')
        self.addLink(left_down_Switch, right_down_Switch, cls = TCLink, bw = 10, delay = '30ms')


topos = {'mytopo': (lambda: MyTopo())}