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
from config import THINGSBOARD_HOST, TOKEN_KEYS, DataEncoder
import config
import redis
from data import Data

# Thingsboard platform credentials
# THINGSBOARD_HOST = '106.12.216.163'  # Change IP Address

attributesTopic = 'v1/devices/me/attributes'
telemetryTopic = 'v1/devices/me/telemetry'
device = local()
mqtt_client = {}
thread_list = []


def on_connect(client, userdata, flags, rc):
    client.subscribe(attributesTopic)


def on_message(client, userdata, msg):

    if msg.topic.startswith(attributesTopic):
        value = json.loads(msg.payload)
        # cur_thread = threading.current_thread()
        token = device._token
        data = Param.getInstance(token, **value)
        print("prepare to send {}".format(data))
        _redis.publish("guolu", str(data))


def setup_conn(token):
    device._token = token

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(token)
    print("mqtt will be connect to {}".format(THINGSBOARD_HOST))
    print("token will be used {}".format(token))

    client.connect(THINGSBOARD_HOST, 1883, 60)
    mqtt_client[token] = client

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


def publish_mqtt(data):
    """publish data to mqtt

    Arguments:
        data {[type]} -- [description]
    """
    groups = data.split("#")
    for index, group in enumerate(groups):
        print("info of group {}".format(group))
        values = [float(x) for x in group.split(",")]
        data = Data(values)
        token = TOKEN_KEYS.get(index)
        client = mqtt_client.get(token)
        p_data = json.dumps(data, indent=4, cls=DataEncoder)
        client.publish(telemetryTopic, p_data, 1)


def sub_redis():
    """[summary]
    """
    _redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    with _redis:
        p = _redis.pubsub(ignore_subscribe_messages=True)
        with p:
            p.subscribe('kalix')
            while True:
                msg = p.get_message()
                if msg:
                    print("get subscribe from redis, value is {}".format(
                        msg['data']))
                    publish_mqtt(msg['data'])
                time.sleep(0.001)


def main():
    try:
        if len(thread_list) == 0:
            run_mqtt()
        sub_redis()
    except:
        print("unable to run")


if __name__ == "__main__":
    main()
