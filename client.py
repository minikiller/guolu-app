#!/usr/bin/env python3
"""
用于测试客户端发送遥测数据

"""
import socket
import time

HOST = 'localhost' 
PORT = 9998      

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    send_data=b'12.12,325.40,83.71,15.52,38.63,76.51,193.03,258.50,258.70#13.11,331.50,83.46,16.38,40.52,79.33,196.36,258.30,258.50#14.08,337.10,83.63,17.21,42.36,85.14,211.88,258.70,258.50#15.10,342.70,83.08,18.18,44.35,89.91,221.76,258.70,258.60'
    # data=b'Polling'
    # s.sendall(send_data)
    print("client is begining ")
    INTERVAL = 30
    print("Thread  Started")
    next_reading = time.time()
    while True:
        print("begin to send")
        s.sendall(send_data)
        # data = s.recv(1024)
        # print('Received', repr(data))
        next_reading += INTERVAL
        sleep_time = next_reading - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

# print('Received', repr(data))