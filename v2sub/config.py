from v2sub import utils

V2RAY_CONFIG_FILE = "/usr/local/etc/v2ray/config.json"


def _get_config(addr: str, port: int, id_: str, alterId="0", network="tcp", type="none", tls="",client_port=1080) -> dict:
    return {
        "inbounds": [
            {
            "listen": "127.0.0.1",
            "protocol": "socks",
            "settings": {
                "ip": "",
                "userLevel": 0,
                "timeout": 360,
                "udp": true,
                "auth": "noauth"
            },
            "port": client_port
            },
        ],
        "outbounds": [
            {
            "mux": {
                "enabled": false,
                "concurrency": 8
            },
            "protocol": "vmess",
            "streamSettings": {
                "tcpSettings": {
                "header": {
                    "type": type
                }
                },
                "tlsSettings": {
                "allowInsecure": true
                },
                "security": tls,
                "network": network
            },
            "tag": "agentout",
            "settings": {
                "vnext": [
                {
                    "address": addr,
                    "users": [
                    {
                        "id": id_,
                        "alterId": alterId,
                        "level": 0,
                        "security": "aes-128-gcm"
                    }
                    ],
                    "port": port
                }
                ]
            }
            },
            {
            "tag": "direct",
            "protocol": "freedom",
            "settings": {
                "domainStrategy": "AsIs",
                "redirect": "",
                "userLevel": 0
            }
            },
            {
            "tag": "blockout",
            "protocol": "blackhole",
            "settings": {
                "response": {
                "type": "none"
                }
            }
            }
        ],
        "dns": {
            "servers": [
            ""
            ]
        },
        "routing": {
            "strategy": "rules",
            "settings": {
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                {
                "outboundTag": "direct",
                "type": "field",
                "ip": [
                    "geoip:cn",
                    "geoip:private"
                ],
                "domain": [
                    "geosite:cn",
                    "geosite:speedtest"
                ]
                }
            ]
            }
        },
        "transport": {}
    }


def update_config(node: dict, client_port: int):
    v2ray_config = _get_config(node['add'], int(node['port']), node['id'], note['aid'], node['net'], node['type'], node['tls']
                               client_port=client_port)
    utils.write_to_json(v2ray_config, V2RAY_CONFIG_FILE)
