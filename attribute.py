
"""参数初始化
"""


class GeneralAttribute:
    """通用参数设置类
    """

    def __init__(self, *params):
        self.Interval = float(params[0])  # 时间间隔
        self.SampleNum = float(params[1])  # 采样数量
        self.Threshold = float(params[2])  # 显示阈值
        self.DeviceNum = params[3]  # 设备编号
        self.Fluid = params[4]  # 被测介质


class SpecAttribute:
    """设备参数设置类
    """

    def __init__(self, *params):
        self.P_Range = float(params[0])  # 压力量程
        self.T_Range = float(params[1])  # 温度量程
        self.KP_Range = float(params[2])  # 孔板差压量程
        self.WP_Range = float(params[3])  # 文管差压量程
        self.In_Dia = float(params[4])  # 管道内径
        self.a_Kb = float(params[5])  # 孔板系数
        self.a_Wg = float(params[6])  # 文管系数
        self.d_Kb = float(params[7])  # 孔板喉径
        self.d_Wg = float(params[8])  # 文管喉径
        self.No_Pipe = params[9]  # "111注汽管网"  # 安装位置
        
