from json import JSONEncoder
import configparser
import tbapi


"""系统的配置参数以及全局常量定义

"""
# 读入配置文件
config = configparser.ConfigParser()
config.read("guolu.conf", encoding="utf-8")
 
THINGSBOARD_HOST = config.get("thingsboard", "host") #'106.12.216.163'
HOST_IP = "http://{}:8080/".format(THINGSBOARD_HOST)

HOST_URL = "http://{}:8080".format(THINGSBOARD_HOST)

THINGSBOARD_USERNAME = config.get("auth", "username")
THINGSBOARD_PASSWORD = config.get("auth", "password")

# access tb api
tbapi = tbapi.TbApi(HOST_URL, THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)


device_A1 = config.get("thingsboard", "device_A1")
device_A2 = config.get("thingsboard", "device_A2")
device_A3 = config.get("thingsboard", "device_A3")
device_A4 = config.get("thingsboard", "device_A4")
setting_device = config.get("thingsboard", "setting_device")
# device_A1 = "39gYWBel4bIyX0aJpyRJ"  # test device 1
# device_A2 = "euA3H8RrGDjt6a1yPt8M"
TOKEN_LIST = [setting_device, device_A1, device_A2, device_A3, device_A4]

TOKEN_KEYS = {
    0: device_A1,
    1: device_A2,
    2: device_A3,
    3: device_A4,
    4: setting_device
}

# TOKEN_KEYS = {
#     0:  "D2zdHCHsbKnGUGxi6U9t"
# }

TOKEN_ITEMS = {
    device_A1: 1,
    device_A2: 2,
    device_A3: 3,
    device_A4: 4
}

# 获得token和deviceid的对应关系dict
device_dict = tbapi.get_device_token_deviceid_dict()

"""用于json格式化dump的类

Returns:
    [type] -- [description]
"""


class DataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
