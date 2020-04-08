#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import time

ip_port = ('127.0.0.1', 9998)

s = socket.socket()     # 创建套接字

with s:
    s.connect(ip_port)  # 连接服务器
    s.sendall(b'Param')

    while True:     # 通过一个死循环不断接收用户输入，并发送给服务器

        server_reply = s.recv(1024).decode()
        print(server_reply)
        time.sleep(0.001)
        

# s.close()       # 关闭连接