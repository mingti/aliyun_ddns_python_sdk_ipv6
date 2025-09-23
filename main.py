#!/usr/bin/env python3
import subprocess
import ipaddress
import json

import aliyun

def get_ipv6_by_ip_command():
    """使用ip命令获取全局IPv6地址"""
    try:
        result = subprocess.run(
            ['ip', '-6', '-json', 'addr', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
        
        interfaces = json.loads(result.stdout)
        ipv6_addresses = []
        
        for interface in interfaces:
            ifname = interface.get('ifname', '')
            for addr_info in interface.get('addr_info', []):
                if addr_info.get('scope') == 'global':
                    ipv6_addresses.append({
                        'interface': ifname,
                        'address': addr_info.get('local', ''),
                        'prefixlen': addr_info.get('prefixlen', '')
                    })
        
        return ipv6_addresses
        
    except Exception as e:
        print(f"错误: {e}")
        return []


def get_ipv6(interface,eui=False):
    """ 指定网络接口获取ipv6, 可指定eui地址"""

    res=[]
    addresses = get_ipv6_by_ip_command()
    for addr in addresses:
        if addr['interface'] == interface or addr['interface'] is None:
            
            if eui:
                if 'ff:fe' in ipaddress.IPv6Address(addr['address']).exploded.lower():
                    res.append(addr['address'])
            else:
                res.append(addr['address'])

    return res



# 使用示例
if __name__ == "__main__":
    eui_address = get_ipv6(interface = 'wlp3s0' , eui = True)[0]
    aliyun.Sample.main()
    print(eui_address)