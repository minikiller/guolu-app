### have to server 
one is for post data
another is for change parameter

socket testing data is:
12.12,325.40,83.71,15.52,38.63,76.51,193.03,258.50,258.70#13.11,331.50,83.46,16.38,40.52,79.33,196.36,258.30,258.50#14.08,337.10,83.63,17.21,42.36,85.14,211.88,258.70,258.50#15.10,342.70,83.08,18.18,44.35,89.91,221.76,258.70,258.60

### server.py
socket server，通过http的post发射遥测数据(暂不使用)
### socket_server.py
通过mqtt接受遥测数据，并监听redis的订阅消息
socket server
### mqtt-client
独立运行，启动mqtt客户端，接受thingsboard端的设备参数修改，同时publish遥测数据

### init_attribute
对设备参数对初始化设置，socket头是UpLoadPara

### 总体概述
本应用主要是负责和thingsboard对接，核心设计是采用mqtt进行数据的传递。
redis负责异步消息，通过两个topic，一个guolu，负责接受tb的参数修改，一个kalix负责遥测数据的传递。

### thingsboard scope
api 地址中的api/plugins/telemetry/DEVICE/{}/SHARED_SCOPE可以是以下的数值
SERVER_SCOPE
SHARED_SCOPE
CLIENT_SCOPE

## todo 
1.config file to read
2.threading monitor

### vim /etc/redis.conf
slave-read-only no