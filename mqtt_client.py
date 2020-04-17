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
import redis_wrapper
from data import Data
import concurrent.futures
from multiprocessing import freeze_support
import logger_mqtt
import socket
# Thingsboard platform credentials
# THINGSBOARD_HOST = '106.12.216.163'  # Change IP Address
"""独立运行的mqtt客户端，遥测数据和参数修改都使用mqtt

Raises:
    SystemError: [description]
"""

attributesTopic = 'v1/devices/me/attributes'
telemetryTopic = 'v1/devices/me/telemetry'
device = local()
mqtt_client = {}
thread_list = []
_logger = logger_mqtt.get_logger(__name__)


def on_log(client, userdata, level, buf):
    _logger.info("log: {},token is {}".format(buf,device._token))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        _logger.error(
            "mqtt disconnection,attempting to reconnect,token is {}".format(device._token))
        try:
            client.reconnect()
        except socket.error as e:
            _logger.error(e)


def on_connect(client, userdata, flags, rc):
    client.subscribe(attributesTopic)


def on_message(client, userdata, msg):

    if msg.topic.startswith(attributesTopic):
        # 当接受到参数修改的topic时候，发送数据给redis的guolu主题
        redis_conn = redis_wrapper.RedisWrapper().redis_connect()
        value = json.loads(msg.payload)
        # cur_thread = threading.current_thread()
        token = device._token
        data = Param.getInstance(token, **value)
        _logger.info("prepare to send {}".format(data))
        redis_conn.publish("guolu", str(data))


def setup_conn(token):
    device._token = token

    client = mqtt.Client()
    client.on_log=on_log # set client logging
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.enable_logger()
    client.username_pw_set(token)
    client.user_data_set(token) # set userdata

    _logger.info("mqtt will connect to {},token will be used {}".format(THINGSBOARD_HOST,token))

    client.connect(THINGSBOARD_HOST, port=1883, keepalive=60)
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
        _logger.error("mqtt is interrupted")
        client.disconnect()


def run_mqtt():
    """创建threading，四个设备建立四个线程

    """

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(setup_conn, TOKEN_LIST)
    for key in config.TOKEN_KEYS:
        k = threading.Thread(target=setup_conn,
                             args=(config.TOKEN_KEYS[key],))
        thread_list.append(k)

    for t in thread_list:
        t.setDaemon(True)
        t.start()
    # 创建redis等待thread
    s = threading.Thread(target=sub_redis)
    s.start()

    for t in thread_list:
        t.join()


def publish_mqtt(data):
    """publish 遥测数据 to mqtt

    Arguments:
        data {[type]} -- [description]
    """
    try:
        groups = data.decode().split("#")
        for index, group in enumerate(groups):
            _logger.info("received telemetry data is {}".format(group))
            values = [float(x) for x in group.split(",")]
            data = Data(values)
            token = TOKEN_KEYS.get(index)
            client = mqtt_client.get(token)
            p_data = json.dumps(data, indent=4, cls=DataEncoder)
            client.publish(telemetryTopic, p_data, 1)
    except Exception as e:
        _logger.error("error is occured {}".format(e))


def sub_redis():
    """循环等待接受redis的遥测数据，redis的主题是kalix
    """
    _redis = redis_wrapper.RedisWrapper().redis_connect()
    with _redis:
        p = _redis.pubsub(ignore_subscribe_messages=True)
        with p:
            p.subscribe('kalix')
            while True:
                msg = p.get_message()
                if msg:
                    _logger.info("get subscribe from redis, value is {}".format(
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
        _logger.info(e)


if __name__ == "__main__":
    # freeze_support()
    main()
