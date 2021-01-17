# -*- coding: utf-8 -*-
import pickle
import numpy as np
import os


class Tool(object):
    FUND_INFO_DICT_PKL = "pkl_data/fund_info_dict.pkl"
    HIGH_RISK_TYPES = ["股票指数", "混合型", "股票型"]

    @classmethod
    def load_fund_info_by_type(cls, fund_types=None, base_path='.'):
        fund_types = fund_types or cls.HIGH_RISK_TYPES
        path = os.path.join(base_path, cls.FUND_INFO_DICT_PKL)
        with open(path, 'rb') as fp:
            fund_info_dict = pickle.load(fp)
        target_funds = {}
        for k, v in fund_info_dict.items():
            if v['type'] in fund_types:
                target_funds[k] = v
        return target_funds

    @staticmethod
    def get_value_list(fund, unit_value=False):
        detail = fund.get("detail")
        date_value = []
        value_name = "unit_value" if unit_value else "cumulative_value"
        for k, v in detail.items():
            date_value.append((k, float(v.get(value_name))))
        date_value.sort(key=lambda x: x[0])
        return [x[1] for x in date_value]


if __name__ == '__main__':
    f = Tool.load_fund_info_by_type()
    print(Tool.get_value_list(f[161725]))
