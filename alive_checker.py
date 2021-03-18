#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Danny0'

import re
import socket
import threading
import requests
from proxy_getter import ProxyGetter
from util.func import *


class CheckProxy(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def check_alive_by_port(ip):
        """
        检查proxy是否可用
        """
        port = ip.split(":")
        if len(port) != 2:
            return False
        ip = port[0]
        port = int(port[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(CHECK_TIMEOUT)
        try:
            s.connect((ip, port))
            s.shutdown(2)
            return True
        except Exception as e:
            log_ins.warning(ip + " port not open")
            return False

    @staticmethod
    def check_alive_by_curl(ip_str):
        """
        检查proxy是否可用
        """
        ips = ip_str.split(":")
        ip = ips[0]
        try:
            res = requests.get("https://www.baidu.com/", timeout=CHECK_TIMEOUT,
                               headers = {
                                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
                                    },
                               proxies={
                                   "http": ip_str,
                                   "https": ip_str
                               })
            #print(res.text)
            if not re.search("全球最大的中文搜索引擎", res.text):
                log_ins.warning(ip + " can't use")
                return False
            else:
                log_ins.info(ip + " proxy is ok ")
                return True
        except:
            log_ins.warning(ip + " can not connected")
            return False

    def run(self):
        log_ins.debug("thread " + str(threading.currentThread().ident) + " start")
        global ip_list
        while len(ip_list) > 0:
            ip = ip_list.pop().decode('utf-8')
            print(ip)
            if not self.check_alive_by_port(ip) or not self.check_alive_by_curl(ip):
                log_ins.warning("remove ip : " + ip)
                redis_ins.zrem(REDIS_KEY, ip)


def check():
    # 启用多线程挨个检测IP存活
    log_ins.debug("start check ip")
    global ip_list
    ip_list = redis_ins.zrange(REDIS_KEY, 0, 10000)
    thread_pool = []
    for i in range(0, CHECK_THREAD_NUM):
        thread_pool.append(CheckProxy())
        thread_pool[i].start()
    for i in range(0, CHECK_THREAD_NUM):
        thread_pool[i].join()
    log_ins.debug("check ip end")


def save(ips):
    """
    保存新ip到redis
    :param ips: 
    :return: 
    """
    for ip in ips:
        mapping = {
        ip : 0,
        }
        redis_ins.zadd(REDIS_KEY, mapping)


if __name__ == '__main__':
    proxy = ProxyGetter()
    redis_ins = get_redis_ins()
    log_ins = get_logger()
    ip_list = []
    check()
    if redis_ins.zcount(REDIS_KEY, 0, 10000) < MIN_IP_NUM:
        log_ins.warn("usable ip num is 0, try get new ip")
        # 可用代理数量小于规定数量，启动获取新IP
        ips = proxy.get_ip(DEFAULT_PROXY, NEW_IP_NUM)
        save(ips)
        check()
