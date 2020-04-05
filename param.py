from enum import Enum, unique


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
    P_Value:9
    Dp_Kb:10
    Dp_Wg:11
    T_Value:12
    Dry_Value:13
    Qm_Value:14
    Acc_Qm_Value:15
    Save:16



@unique
class GeneralType(Enum):
    Interval: 0  # 时间间隔
    SampleNum: 1  # 采样数量
    Threshold: 2  # 显示阈值
    DeviceNum: 3  # 设备编号
    Fluid: 4  # 被测介质

# general_type=[""]


class Param:
    def __init__(self, index, name, value):
        self.header = "####"
        self.number = "1234"
        self.username = "hbh"
        self.password = "1216"
        self._index = index  # 0,all ,1,2,3,4
        self._name = name
        self._value = value
        self._uuid = 80800
        self.tail = "####"

    def toStr(self):
        temp = self.__dict__.values()
        result = ','.join(str(n) for n in temp)
        return result


def main():
    hello = Param(0, "INterval", 15)
    print(hello.toStr())


if __name__ == "__main__":
    main()
# spec_param=
