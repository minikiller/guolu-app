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
import config
import redis

# Thingsboard platform credentials
# THINGSBOARD_HOST = '106.12.216.163'  # Change IP Address

attributesTopic = 'v1/devices/me/attributes'
device = local()
global_store = {}
thread_list =[]
_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


# MQTT on_connect callback function
# socketCon = None   # socket connection

# class Device:
#     def __init__(self, token):
#         self._token = token


def on_connect(client, userdata, flags, rc):
    #print("rc code:", rc)
    # client.subscribe('v1/devices/me/rpc/request/+')
    client.subscribe(attributesTopic)

# def change_conn(link):
#     global socketCon
#     socketCon=link


def on_message(client, userdata, msg):

    if msg.topic.startswith(attributesTopic):
        value = json.loads(msg.payload)
        # cur_thread = threading.current_thread()
        token = device._token
        data = Param.getInstance(token, **value)
        print("prepare to send {}".format(data))
        # link.sendall(str(test).encode())
        _redis.publish("guolu", str(data))
        # socketCon.sendall(.encode())
        # data = socketCon.recv(1024)
        # print("receive data is "+data.decode())


def setup_conn(token):
    # create a client instance
    # cur_thread = threading.current_thread()
    # global global_store
    # global_store[id(cur_thread)] = token
    # print(id(socket_con))
    # global device
    device._token = token
    # socketCon = socket_con

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(token)
    print("mqtt will be connect to {}".format(THINGSBOARD_HOST))
    print("token will be used {}".format(token))

    client.connect(THINGSBOARD_HOST, 1883, 60)

    # t = Thread(target=publishValue, args=(client,))

    try:
        # client.loop_start()
        client.loop_forever()

        # t.start()
        # while True:
        #     # if socketCon._closed:
        #     #     raise SystemError("no connection is actived")
        #     pass

    except KeyboardInterrupt:
        client.disconnect()

def run_mqtt():
    for key in config.TOKEN_KEYS:
        k = threading.Thread(target=setup_conn,
                             args=(config.TOKEN_KEYS[key],))
        thread_list.append(k)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

def main():
    try:
        if len(thread_list) == 0:
            run_mqtt()
    except:
        print("unable to run")


if __name__ == "__main__":
    main()
