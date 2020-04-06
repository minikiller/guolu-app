#!/usr/bin/env python3

import socket

HOST = '192.168.1.34' 
PORT = 9999      

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # data=b'12.12,325.40,83.71,15.52,38.63,76.51,193.03,258.50,258.70#13.11,331.50,83.46,16.38,40.52,79.33,196.36,258.30,258.50#14.08,337.10,83.63,17.21,42.36,85.14,211.88,258.70,258.50#15.10,342.70,83.08,18.18,44.35,89.91,221.76,258.70,258.60'
    data=b'Polling'
    s.sendall(data)
    print("client is begining ")
    while True:
        data = s.recv(1024)
        print('Received', repr(data))

print('Received', repr(data))