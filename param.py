from enum import Enum, unique
import uuid
import config
from config import tbapi, device_dict


@unique
class SpecType(Enum):
    P_Range: 0  # 压力量程
    T_Range: 1  # 温度量程
    KP_Range: 2  # 孔板差压量程
    WP_Range: 3  # 文管差压量程
    In_Dia: 4  # 管道内径
    a_Kb: 5  # 孔板系数
    a_Wg: 6  # 文管系数
    d_Kb: 7  # 孔板喉径
    d_Wg: 8  # 文管喉径
    No_Pipe: 9  # "111注汽管网"  # 安装位置
    P_Value: 10  # 压力值     
    Dp_Kb: 11  #  孔板差压值    
    Dp_Wg: 12  #  文管差压值   
    T_Value: 13  #  温度值  
    Dry_Value: 14  #  干度值
    Qm_Value: 15  #  流量值 
    Acc_Qm_Value: 16  #  累积流量值


@unique
class GeneralType(Enum):
    Interval: 0  # 时间间隔
    SampleNum: 1  # 采样数量
    Threshold: 2  # 显示阈值
    DeviceNum: 3  # 设备编号
    Fluid: 4  # 被测介质


general_param = ("Interval", "SampleNum", "Threshold", "DeviceNum", "Fluid")

spec_param = ("P_Range", "T_Range", "KP_Range", "WP_Range",
              "In_Dia", "a_Kb", "a_Wg", "d_Kb",
              "d_Wg", "No_Pipe", "P_Value", "Dp_Kb", "Dp_Wg",
              "T_Value", "Dry_Value", "Qm_Value", "Acc_Qm_Value")


class Param:

    def __init__(self, index, name, value):
        self.header = "####"
        self.number = "1234"
        self.username = "hbh"
        self.password = "1216"
        self._index = index  # 0,all ,1,2,3,4
        self._name = name
        self._value = value
        self._uuid = uuid.uuid1()
        self.tail = "####"

    @classmethod
    def getInstance(cls, token, **params):
        index = config.TOKEN_ITEMS.get(token)

        for key in params:
            if key == 'No_Pipe':
                # device name change,not send to socket client
                global device_dict
                device_id = device_dict[token]
                tbapi.change_device_name(device_id, params[key])
                return None
            if key in general_param:
                return cls(0, key, params[key])
            elif key in spec_param:
                return cls(index, key, params[key])
            else:
                raise AttributeError()

    def __str__(self):
        temp = self.__dict__.values()
        result = ','.join(str(n) for n in temp)
        return result


def main():
    # hello = Param(0, "Interval", 15)
    # print(hello.__dict__)
    value = {"Interval1": 15}
    ACCESS_TOKEN = "39gYWBel4bIyX0aJpyRJ"
    data = Param.getInstance(ACCESS_TOKEN, **value)
    print(str(data))


if __name__ == "__main__":
    main()
