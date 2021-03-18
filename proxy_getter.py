#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from util.func import *
import json

__author__ = 'Danny0'


class ProxyGetter():
    proxy_source = [
        "tudoudaili",
        "kuaidaili"
    ]

    def __init__(self):
        self.log_ins = get_logger()
        pass

    def get_ip(self, source, num):
        if source not in self.proxy_source:
            return False
        ips = eval("self.from_" + source + "(num)")
        self.log_ins.debug("got new ip num : " + str(len(ips)))
        return ips

    def from_tudoudaili(self, num):
        self.log_ins.debug("start get new ip from tudoudaili")
        api = "http://tvp.daxiangdaili.com/ip/"
        param = {
            "tid": ORDER_ID_TUDOU,
            "num": num,
            "area": "",
            "foreign": "all",
            "ports": "",
            "exclude_ports": "",
            "protocol": "",
            "filter": "on"
        }
        res = requests.get(api, param)
        if res.text[0:5] == "ERROR":
            return []
        ips = res.text.split("\r\n")
        return ips

    def from_kuaidaili(self, num):
        self.log_ins.debug("start get new ip from jiangxianli")
        ips = []
        api = "https://ip.jiangxianli.com/api/proxy_ips"
        param = {
            "page": 1,
            "country": "",
            "isp": "",
            "order_by": "validated_at",
            "order_rule": ""
        }
        res = requests.get(api, param)
        ips_data = json.loads(res.text)
        for ipdata in ips_data['data']['data']:
            ips.append(ipdata['ip']+":"+ipdata['port'])
        return ips

'''
    def from_kuaidaili(self, num):
        """
        获取代理ip列表
        """
        list_ips=[]
        self.log_ins.debug("start get new ip from kuaidaili")
        for i in range(3):
            api = "https://www.kuaidaili.com/free/intr/"+str(i+1)
            res = requests.get(api, headers={
                "Accept-Encoding": "gzip"
            })
            soup = BeautifulSoup(res.text,"html.parser")
            list_ip=[]
            list_port=[]        
            for tag in soup.find_all(attrs={"data-title":'IP'}):
                list_ip.append(tag.get_text())
            for tag in soup.find_all(attrs={"data-title":'PORT'}):
                list_port.append(tag.get_text())
            for i in range(len(list_ip)):
                list_ips.append(list_ip[i]+":"+list_port[i])
            time.sleep(10)
        print(list_ips)
        return list_ips
'''


if __name__ == '__main__':
    getter = ProxyGetter()
    print(getter.get_ip("tudoudaili", 2))
