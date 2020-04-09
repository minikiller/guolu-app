import http_req as req
from config import TOKEN_KEYS

class Data:

    def __init__(self, value):
        # self.type = value[0]  # type
        # self._index=index
        self.P_Value = value[0]  # 工作压力
        self.T_Value = value[1]  # 工作温度
        self.Dry_Value = value[2]  # 蒸汽干度
        self.Qm_Value = value[3]  # 质量流量
        self.Qh_Value = value[4]  # 载热流量
        self.Acc_Qm_Value = value[5]  # 累积流量
        self.Qh_Qh_Value = value[6]  # 载热流量
        self.Deltp_KB = value[7]  # 孔板差压
        self.Deltp_WG = value[8]  # 文管差压

    def post(self, index):
        req.post_data(TOKEN_KEYS.get(index), self)
