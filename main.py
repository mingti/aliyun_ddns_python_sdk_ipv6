#!/usr/bin/env python3
import os
import subprocess
import ipaddress
import json

import aliyun
from log import logger




def get_ipv6_by_ip_command():
    """使用ip命令获取全局IPv6地址"""

    ipv6_addresses = []
    try:
        result = subprocess.run(
            ['ip', '-6', '-json', 'addr', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
        
        interfaces = json.loads(result.stdout)
        
        for interface in interfaces:
            ifname = interface.get('ifname', '')
            for addr_info in interface.get('addr_info', []):
                if addr_info.get('scope') == 'global':
                    ipv6_addresses.append({
                        'interface': ifname,
                        'address': addr_info.get('local', ''),
                        'prefixlen': addr_info.get('prefixlen', '')
                    })
        
        
    except Exception as e:
        logger.error("获取本机ip失败",e)
        
    
    return ipv6_addresses


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


def main():

    # 获取eui地址
    eui_address = get_ipv6(interface = os.environ["LOCAL_IPV6_INTERFACE"] , eui = True)[0]

    # 获取阿里云解析中的地址
    dns_id_ip=aliyun.OpenAPI.describe_domain_records_id_and_ip(domain_name=os.environ['DOMAIN_NAME'], rrkey_word=os.environ['DONAIN_RR'], type=os.environ['DNS_TYPE'])

    if eui_address !=dns_id_ip['value']:
        aliyun.OpenAPI.update_domain_record(record_id=dns_id_ip['record_id'], rrkey_word=os.environ['DONAIN_RR'], type=os.environ['DNS_TYPE'], value=eui_address)
        logger.info(f"当前IP:{eui_address} , 解析IP:{dns_id_ip['value']} , 需要更新")
    else:
        logger.info(f"当前IP:{eui_address} , 解析IP:{dns_id_ip['value']} , 无需更新")




# 使用示例
if __name__ == "__main__":
    main() 