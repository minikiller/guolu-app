
import requests
import json
from config import HOST_IP
"""
初始化shared属性，通过调用token
"""


AUTH_ADDRESS = HOST_IP + "api/auth/login"

DEVICE_ID_A1 = "b3bcb810-56cf-11ea-9eca-97bfcfb9f3d0"
DEVICE_ID_A2 = "b93fda10-56cf-11ea-9eca-97bfcfb9f3d0"
DEVICE_ID_A3 = "bf2d0880-56cf-11ea-9eca-97bfcfb9f3d0"
DEVICE_ID_A4 = "c62a6e70-56cf-11ea-9eca-97bfcfb9f3d0"

device_list=(DEVICE_ID_A1,DEVICE_ID_A2,DEVICE_ID_A3,DEVICE_ID_A4)
auth_data = {"username": "sunlingfeng@xcloudlive.com", "password": "123456"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
shared_address = HOST_IP + "api/plugins/telemetry/DEVICE/{}/SHARED_SCOPE"

shared_device_attribute = {
    "P_Range": 32,
    "T_Range": 500,
    "KP_Range": 500,
    "WP_Range": 500,
    "In_Dia": 51,
    "a_Kb": 0.67133,
    "a_Wg": 1.01334,
    "d_Kb": 34.68,
    "d_Wg": 28.56,
    "No_Pipe": "111注汽管网",
    "P_Modify": 10,  # 压力值     
    "Dp_Kb": 11,  #  孔板差压值    
    "Dp_Wg": 12,  #  文管差压值   
    "T_Value": 13,  #  温度值  
    "Dry_Value": 14,  #  干度值 
    "Qm_Value": 15,  #  流量值 
    "Acc_Qm_Value": 16,  #  累积流量值
}

shared_attribute = {
    "Location": "52-14井口",
    "Fluid": "湿蒸汽",
    "Interval": 1,
    "SampleNum": 256,
    "Threshold": 25
}
"""get auth token
"""
r_data = json.dumps(auth_data, indent=4)
print("send json data is {}".format(r_data))
r = requests.post(AUTH_ADDRESS,
                  data=r_data, headers=headers)
print(r.content)
data = json.loads(r.content)
token = data['token']

headers['x-authorization'] = 'Bearer ' + token

r_data = json.dumps(shared_device_attribute, indent=4)
for device_id in device_list:
    print("send json data is {}".format(r_data))
    addr = shared_address.format(device_id)
    print("send addr is {}".format(addr))
    
    r = requests.post(addr,
                    data=r_data, headers=headers)
    print(r.status_code)
