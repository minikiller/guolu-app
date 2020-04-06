#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from data import Data
from param import Param
import post
import config

# reload(sys)

# sys.setdefaultencoding('utf-8')
import socket
import threading        # 导入线程模块


def link_handler(link, client):
    """
    该函数为线程需要执行的函数，负责具体的服务器和客户端之间的通信工作
    :param link: 当前线程处理的连接
    :param client: 客户端ip和端口信息，一个二元元组
    :return: None
    """
    print("服务器开始接收来自[%s:%s]的请求...." % (client[0], client[1]))
    while True:     # 利用一个死循环，保持和客户端的通信状态
        client_data = link.recv(1024).decode()
        if client_data == "exit":
            print("结束与[%s:%s]的通信..." % (client[0], client[1]))
            break
        elif client_data == "Polling":
            # link.sendall('NOP'.encode())
            change_param(link)
        elif ":" in client_data:
            parse_data(client_data)
        elif "#" in client_data:
            post_data(link, client_data)
        else:
            pass
        # :
        #     print("来自[%s:%s]的客户端向你发来信息：%s" %
        #           (client[0], client[1], client_data))
    link.close()


def parse_data(client):  # return code,begin with : and spilt with #
    print(client)
    value = client.split("#")
    print("serial is {}".format(value[0]))
    print("status is {}".format(value[1]))  # Done, Err


def change_param(link):
    test = Param(0, "Interval", 15)
    print("prepare to send {}".format(test))
    link.sendall(str(test).encode())


def post_data(link, client_data):
    groups = client_data.split("#")
    for index, group in enumerate(groups):
        print("info of group {}".format(group))
    # if values[0] == "data":

        values = [float(x) for x in group.split(",")]
        data = Data(values)
        # print(data.__dict__)
        data.post(index)
        # print(data.__dict__)
    link.sendall('ok'.encode())


def run_mqtt(conn):

    """ create mqtt client listen for parameter change message
    :type conn:
    :param conn:

    :raises:

    :rtype:
    """
    thread_list = []
    for key in config.TOKEN_KEYS:
        k = threading.Thread(target=post.setup_conn,
                             args=(conn, config.TOKEN_KEYS[key]))
        thread_list.append(k)
    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()


ip_port = ('0.0.0.0', 9999)
sk = socket.socket()            # 创建套接字
sk.bind(ip_port)                # 绑定服务地址
sk.listen(5)                    # 监听连接请求

print('启动socket服务，等待客户端连接...')

while True:     # 一个死循环，不断的接受客户端发来的连接请求
    conn, address = sk.accept()  # 等待连接，此处自动阻塞
    # 每当有新的连接过来，自动创建一个新的线程，
    # 并将连接对象和访问者的ip信息作为参数传递给线程的执行函数
    print(id(conn))
    t = threading.Thread(target=link_handler, args=(conn, address))
    t.start()
    run_mqtt(conn)
