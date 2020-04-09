# mqtt客户端，负责独立运行，接受mqtt的消息
import os
import time
import sys
import json
import random
import paho.mqtt.client as mqtt
from threading import Thread, local
from param import Param
import threading
from config import THINGSBOARD_HOST, TOKEN_KEYS, DataEncoder, TOKEN_LIST
import config
import redis
from data import Data
import concurrent.futures
from multiprocessing import freeze_support
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
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        value = json.loads(msg.payload)
        # cur_thread = threading.current_thread()
        token = device._token
        data = Param.getInstance(token, **value)
        print("prepare to send {}".format(data))
        redis_conn.publish("guolu", str(data))


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
        print("mqtt is interrupted")
        client.disconnect()


def run_mqtt():

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(setup_conn, TOKEN_LIST)
    for key in config.TOKEN_KEYS:
        k = threading.Thread(target=setup_conn,
                             args=(config.TOKEN_KEYS[key],))
        thread_list.append(k)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    s = threading.Thread(target=sub_redis)
    s.start()
    for t in thread_list:
        t.join()


def publish_mqtt(data):
    """publish data to mqtt

    Arguments:
        data {[type]} -- [description]
    """
    groups = data.decode().split("#")
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


def runit():
    pass

def main():
    try:
        run_mqtt()
        # sub_redis()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # freeze_support()
    main()
