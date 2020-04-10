from json import JSONEncoder

"""系统的配置参数以及全局常量定义

"""

THINGSBOARD_HOST = '106.12.216.163'
HOST_IP = "http://{}:8080/".format(THINGSBOARD_HOST)

device_A1 = "9Lqw5CLDl7aAwApTf0ml"
device_A2 = "3p9za71mK8IDCFtnDbQR"
device_A3 = "U8xoyQCM62XM3qQKtCH3"
device_A4 = "1PJWAwwBe69uVItx4i1p"
setting_device = "fwrrFIO0Y9A4ke3ukgQ4"
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

TOKEN_ITEMS = {
    device_A1: 1,
    device_A2: 2,
    device_A3: 3,
    device_A4: 4
}

"""用于json格式化dump的类

Returns:
    [type] -- [description]
"""


class DataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
