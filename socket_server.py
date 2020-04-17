#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""socket 连接主程序
负责接受客户端的连接，独立运行
"""
import socket
import threading  # 导入线程模块
import redis_get as _redis
import config
import redis_wrapper
import multiprocessing
import mqtt_client
import logger
import init_attribute

thread_list = []
mqtt_thread = None
_logger = logger.get_logger(__name__)


def publish_to_redis(link, client_data):
    """发送数据到redis

    Arguments:
        link {[type]} -- [description]
        client_data {[type]} -- [description]
    """
    redis_conn = redis_wrapper.RedisWrapper().redis_connect()
    redis_conn.publish("kalix", client_data)


def link_handler(link, client):
    """
    该函数为线程需要执行的函数，负责具体的服务器和客户端之间的通信工作
    :param link: 当前线程处理的连接
    :param client: 客户端ip和端口信息，一个二元元组
    :return: None
    """
    _logger.info("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    with link:
        try:
            while True:     # 利用一个死循环，保持和客户端的通信状态
                data = link.recv(1024)
                if not data:
                    _logger.info("结束与[%s:%s]的通信, breaking..." % (client[0], client[1]))
                    break
                else:
                    client_data = data.decode()
                    # _logger.info("new client is connected,info is {},{}".format(
                    #     client[0], client[1]))

                if client_data == "Exit":
                    _logger.info("结束与[%s:%s]的通信..." % (client[0], client[1]))
                    break
                elif client_data == "Polling":  # 负责接受tb端的参数修改
                    global mqtt_thread
                    if mqtt_thread is None or not mqtt_thread.isAlive():
                        mqtt_thread = threading.Thread(
                            target=_redis.sub_msg, args=(link,))
                        mqtt_thread.start()
                    else:
                        pass
                    # elif mqtt_thread.isAlive():
                    link.sendall(b'nop')
                elif "UpLoadPara" in client_data:  # 负责初始化设备的共享参数
                    temp_thread = threading.Thread(
                        target=init_attribute.send_param_to_tb, args=(client_data,))
                    temp_thread.start()
                elif "#" in client_data:  # 负责接受遥测数据
                    publish_to_redis(link, client_data)
                    # link.sendall(b'ok')

                _logger.info("来自[%s:%s]的客户端向你发来信息：\n %s" %
                            (client[0], client[1], client_data))
        except ConnectionResetError:
            _logger.error("connection is closed {}".format(client[0]))
            link.close()
        except socket.error as msg:
            _logger.error("socket error is occured, msg is "+msg)
            link.close()
            link = None
            # link.sendall('服务器 server has recevied your message 123'.encode())


def main():
    # 启动mqtt子进程
    # multiprocessing.freeze_support()
    # p = multiprocessing.Process(target=mqtt_client.main)
    # p.start()
    # p.join()

    ip_port = ('0.0.0.0', 9998)
    sk = socket.socket()            # 创建套接字
    sk.bind(ip_port)                # 绑定服务地址
    sk.listen(5)  # 监听连接请求

    _logger.info('启动socket服务，等待客户端连接...')

    while True:     # 一个死循环，不断的接受客户端发来的连接请求
        conn, address = sk.accept()  # 等待连接，此处自动阻塞
        # 每当有新的连接过来，自动创建一个新的线程，
        # 并将连接对象和访问者的ip信息作为参数传递给线程的执行函数

        t = threading.Thread(target=link_handler, args=(conn, address))
        t.start()


if __name__ == "__main__":
    main()
