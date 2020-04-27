#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import time

ip_port = ('127.0.0.1', 9998)

s = socket.socket()     # 创建套接字
INTERVAL = 10
print("Thread  Started")
next_reading = time.time()
with s:
    s.connect(ip_port)  # 连接服务器
    

    while True:     # 通过一个死循环不断接收用户输入，并发送给服务器
        s.sendall(b'Polling')
        server_reply = s.recv(1024).decode()
        print(server_reply)
        next_reading += INTERVAL
        sleep_time = next_reading - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        

# s.close()       # 关闭连接