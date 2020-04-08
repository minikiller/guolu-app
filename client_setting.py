#!/usr/bin/env python3
"""test for socket client for change parameter
"""

import socket
import time

HOST = 'localhost' 
PORT = 9999      

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # send_data=b'12.12,325.40,83.71,15.52,38.63,76.51,193.03,258.50,258.70#13.11,331.50,83.46,16.38,40.52,79.33,196.36,258.30,258.50#14.08,337.10,83.63,17.21,42.36,85.14,211.88,258.70,258.50#15.10,342.70,83.08,18.18,44.35,89.91,221.76,258.70,258.60'
    send_data=b'Param'
    s.sendall(send_data)
    print("client is begining ")
    
    while True:
        try:
            print("begin to waitting")
            # s.sendall(send_data)
            data = s.recv(1024)
            if not data:
                break
            if "####" in data.decode():
                print("get it")
                s.sendall(b":291f2218-78cd-11ea-8a09-34e6d76a8659#Done")
            print('Received', repr(data))
        except KeyboardInterrupt:
            s.close()
            print('Keyboard Interrupt')
            break            

# print('Received', repr(data))