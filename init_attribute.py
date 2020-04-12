
import requests
import json
from config import HOST_IP, DataEncoder
import logger
import attribute
"""
初始化shared属性，通过调用token
"""
_logger = logger.get_logger(__name__)


AUTH_ADDRESS = HOST_IP + "api/auth/login"

VIRTUAL_DEVICE_ID = "fe3d1840-5aa2-11ea-b86d-79a79971f7b7"

DEVICE_ID_A1 = "b3bcb810-56cf-11ea-9eca-97bfcfb9f3d0"
DEVICE_ID_A2 = "b93fda10-56cf-11ea-9eca-97bfcfb9f3d0"
DEVICE_ID_A3 = "bf2d0880-56cf-11ea-9eca-97bfcfb9f3d0"
DEVICE_ID_A4 = "c62a6e70-56cf-11ea-9eca-97bfcfb9f3d0"

# device_id_list=("03dd1a80-7bf4-11ea-aa25-ad673d3fddf6",)
device_id_list = (VIRTUAL_DEVICE_ID, DEVICE_ID_A1,
                  DEVICE_ID_A2, DEVICE_ID_A3, DEVICE_ID_A4)

auth_data = {"username": "sunlingfeng@xcloudlive.com", "password": "123456"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
shared_address = HOST_IP + "api/plugins/telemetry/DEVICE/{}/SHARED_SCOPE"
# 删除attribute的url地址，后面跟key数值，以逗号分割
# del_shared_address = HOST_IP + "api/plugins/telemetry/DEVICE/{}/SHARED_SCOPE?keys=DeviceNum,Interval"
del_shared_address = HOST_IP + \
    "api/plugins/telemetry/DEVICE/{}/SHARED_SCOPE?keys=P_Modify"


shared_device_attribute = {
    "P_Range": 32,
    "T_Range": 500,
    "KP_Range": 500,
    "WP_Range": 500,
    "In_Dia": 51,
    "a_Kb": 0.670133,
    "a_Wg": 1.01334,
    "d_Kb": 34.68,
    "d_Wg": 28.56,
    "No_Pipe": "111注汽管网",
    "P_Value": 10,  # 压力值     
    "Dp_Kb": 11,  #  孔板差压值    
    "Dp_Wg": 12,  #  文管差压值   
    "T_Value": 13,  #  温度值  
    "Dry_Value": 14,  #  干度值 
    "Qm_Value": 15,  #  流量值 
    "Acc_Qm_Value": 16,  #  累积流量值
}

shared_attribute = {
    "Interval": 1,
    "SampleNum": 256,
    "Threshold": 25,
    "DeviceNum": "1234",
    "Fluid": "湿蒸汽",
}

# 032.00,500.00,500.00,500.00,051.00,0.670133,1.013340,034.68,028.56,11注汽管网
# 032.00,500.00,500.00,500.00,051.00,0.670133,1.013340,034.68,028.56,12注汽管网
# 032.00,500.00,500.00,500.00,051.00,0.670133,1.013340,034.68,028.56,13注汽管网
# 032.00,500.00,500.00,500.00,051.00,0.670133,1.013340,034.68,028.56,14注汽管网
"""get auth token
"""


def getAuth():
    r_data = json.dumps(auth_data, indent=4)
    _logger.info("send json data is {}".format(r_data))
    r = requests.post(AUTH_ADDRESS,
                      data=r_data, headers=headers)
    _logger.info(r.content)
    data = json.loads(r.content)
    token = data['token']

    headers['x-authorization'] = 'Bearer ' + token
    return headers


def init_attribute(headers):
    r_data = json.dumps(shared_device_attribute, indent=4)
    for device_id in device_id_list:
        print("send json data is {}".format(r_data))
        addr = shared_address.format(device_id)
        print("send addr is {}".format(addr))

        r = requests.post(addr,
                          data=r_data, headers=headers)
        _logger.info(r.status_code)


def main():
    init_attribute(getAuth())


def delete(headers):
    for device_id in device_id_list:
        # print("send json data is {}".format(r_data))
        addr = del_shared_address.format(device_id)
        r = requests.delete(addr, headers=headers)
        _logger.info(r.status_code)


def send_param_to_tb(data):
    groups = data.split("#")
    # 忽略groups[0]
    general_list = groups[1].split(",")
    _logger.info("general attribute data is {}".format(general_list))
    general_att = attribute.GeneralAttribute(*general_list)  # 通用参数
    data_list = []
    data_list.append(general_att)
    _groups = groups[2:]
    for index, group in enumerate(_groups):
        list=group.split(",")
        _logger.info("spec attribute data is {}".format(list))
        spec_att = attribute.SpecAttribute(*list)
        data_list.append(spec_att)
        # values = [float(x) for x in group.split(",")]
    headers = getAuth()

    for index, data in enumerate(data_list):
        r_data = json.dumps(data, indent=4, cls=DataEncoder)
        _logger.info("send json data is {}".format(r_data))
        addr = shared_address.format(device_id_list[index])
        _logger.info("send addr is {}".format(addr))

        r = requests.post(addr,
                          data=r_data, headers=headers)
        _logger.info("device id {},return status is {}".format(
            device_id_list[index], r.status_code))


if __name__ == "__main__":
    # delete(getAuth())
    main()
