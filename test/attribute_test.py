#!/usr/bin/env python3
"""
用于测试客户端发送遥测数据

"""
import socket
import time
import sys
import os

sys.path.append("..")
sys.path.extend([os.path.join(root, name)
                 for root, dirs, _ in os.walk("../") for name in dirs])

HOST = 'localhost'
PORT = 9998

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    send_data = 'UpLoadPara#001.00,256.00,025.00,1234.00,湿蒸汽#032.00,500.00,500.00,0.670133,034.68,500.00,1.013340,028.56,051.00,11注汽管网#032.00,500.00,500.00,0.670133,034.68,500.00,1.013340,028.56,051.00,12注汽管网#032.00,500.00,500.00,0.670133,034.68,500.00,1.013340,028.56,051.00,13注汽管网#032.00,500.00,500.00,0.670133,034.68,500.00,1.013340,028.56,051.00,14注汽管网'
    # data=b'Polling'
    # s.sendall(send_data)
    print("client is begining ")
    INTERVAL = 600
    print("Thread  Started")
    next_reading = time.time()
    while True:
        print("begin to send")
        s.sendall(send_data.encode())
        # data = s.recv(1024)
        # print('Received', repr(data))
        next_reading += INTERVAL
        sleep_time = next_reading - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

# print('Received', repr(data))
