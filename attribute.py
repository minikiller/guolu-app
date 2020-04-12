
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
        self.a_Kb = float(params[3])  # 孔板系数
        self.d_Kb = float(params[4])  # 孔板喉径
        self.WP_Range = float(params[5])  # 文管差压量程
        self.a_Wg = float(params[6])  # 文管系数
        self.d_Wg = float(params[7])  # 文管喉径
        self.In_Dia = float(params[8])  # 管道内径
        self.No_Pipe = params[9]  # "111注汽管网"  # 安装位置
        
