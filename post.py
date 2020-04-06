# This Program illustrates the Server Side RPC on ThingsBoard IoT Platform
# Paste your ThingsBoard IoT Platform IP and Device access token
# Temperature_Controller_Server_Side_RPC.py : This program illustrates Server side RPC using a Simulated Temperature Controller
import os
import time
import sys
import json
import random
import paho.mqtt.client as mqtt
from threading import Thread, local
from param import Param
import threading
from config import THINGSBOARD_HOST

# Thingsboard platform credentials
# THINGSBOARD_HOST = '106.12.216.163'  # Change IP Address

attributesTopic = 'v1/devices/me/attributes'
device = local()
global_store = {}

# MQTT on_connect callback function
socketCon = None   # socket connection

# class Device:
#     def __init__(self, token):
#         self._token = token


def on_connect(client, userdata, flags, rc):
    #print("rc code:", rc)
    # client.subscribe('v1/devices/me/rpc/request/+')
    client.subscribe(attributesTopic)


def on_message(client, userdata, msg):

    if msg.topic.startswith(attributesTopic):
        value = json.loads(msg.payload)
        cur_thread = threading.current_thread()
        token = global_store.get(id(cur_thread))
        data = Param.getInstance(token, **value)
        print("prepare to send {}".format(data))
        # link.sendall(str(test).encode())
        socketCon.sendall(str(data).encode())


def setup_conn(socket_con, token):
    # create a client instance
    cur_thread = threading.current_thread()
    global socketCon, global_store
    global_store[id(cur_thread)] = token
    print(id(socket_con))
    # global device
    device.cur_token = token
    socketCon = socket_con

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(token)
    print("mqtt will be connect to {}".format(THINGSBOARD_HOST))
    print("token will be used {}".format(token))

    client.connect(THINGSBOARD_HOST, 1883, 60)

    # t = Thread(target=publishValue, args=(client,))

    try:
        client.loop_forever()
        # t.start()
        while True:
            pass

    except KeyboardInterrupt:
        client.disconnect()


def main():
    try:
        k = Thread(target=setup_conn, args=("conn",))
        k.start()
    except:
        print("unable to run")


if __name__ == "__main__":
    main()
