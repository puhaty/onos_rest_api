def create_json(priority, timeout, deviceId, out_port, ip_dst):
    json = {
        "priority": priority,
        "timeout": timeout,
        "isPermanent": 'true',
        "deviceId": "of:" + deviceId,
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": out_port
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "ETH_TYPE",
                    "ethType": "0x0800"
                },
                {
                    "type": "IPV4_DST",
                    "ip": ip_dst + "/32"
                }
            ]
        }
    }
    return json