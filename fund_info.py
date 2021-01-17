# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import copy
import pandas as pd


class FuncInfo(object):
    def __init__(self, code, name=None, fund_type=None):
        self.code = code,                           # 基金代码
        self.name = name                            # 基金名
        self.fund_type = fund_type                  # 类型
        self._unit_value_ls = []                    # 单位净值list
        self._cumulative_value_ls = []              # 累计净值list
        self._daily_growth_rate_ls = []             # 日增长率
        self._date_ls = []                          # 交易日list
        self._date2idx_map = {}                     # 交易日 -> 单位净值list/累计净值list.. idx

    def clear_data(self):
        self._unit_value_ls = []
        self._cumulative_value_ls = []
        self._daily_growth_rate_ls = []
        self._date_ls = []
        self._date2idx_map = {}

    @staticmethod
    def _parse_date(date, fmt):
        if isinstance(date, datetime):
            date = date.strftime(fmt)
        if not isinstance(date, str):
            raise Exception("date type(%s) error, required: datetime or str" % type(date))
        return date

    def _date2idx(self, date):
        date = self._parse_date(date, "%Y-%m-%d")
        return self._date2idx_map.get(date)

    def get_unit_value(self, date):
        idx = self._date2idx(date)
        return None if idx is None else self._unit_value_ls[idx]

    def get_cumulative_value(self, date):
        idx = self._date2idx(date)
        return None if idx is None else self._cumulative_value_ls[idx]

    def get_daily_growth_rate(self, date):
        idx = self._date2idx(date)
        return None if idx is None else self._daily_growth_rate_ls[idx]

    def load_net_value_info(self, start_date, end_date):
        url = "http://fund.eastmoney.com/f10/F10DataApi.aspx"
        date_fmt = "%Y-%m-%d"
        info = {
            "type": "lsjz",
            "code": self.code,
            "per": 49,
            "sdate": self._parse_date(start_date, date_fmt),
            "edate": self._parse_date(end_date, date_fmt),
        }
        page = 0
        # fp = open("./output/fund_info/%s_%s_raw.txt" % (self.code, self.name), "w")
        update_flag = True
        while update_flag:
            page = page + 1
            update_flag = False
            info["page"] = page
            r = requests.get(url, info)
            soup = BeautifulSoup(r.text, 'lxml')
            th_list = None
            for idx, tr in enumerate(soup.find_all('tr')):
                if idx == 0:
                    th_list = [x.text for x in tr.find_all("th")]
                else:
                    tds = tr.find_all('td')
                    values = [w.text for w in tds]
                    if values[0] == "暂无数据!":
                        break
                    dict_data = dict(zip(th_list, values))
                    # fp.write("%s\n" % dict_data)
                    date = dict_data.get("净值日期")
                    if date and not self._date2idx_map.get(date):
                        self._date2idx_map[dict_data.get("净值日期")] = len(self._unit_value_ls)
                        self._unit_value_ls.append(dict_data.get("单位净值"))
                        self._cumulative_value_ls.append(dict_data.get("累计净值"))
                        self._date_ls.append(date)
                        self._daily_growth_rate_ls.append(dict_data.get("日增长率"))
                        update_flag = True

    def get_data_frame(self):
        date_list = self._date_ls
        df = pd.DataFrame({
            "净值日期": date_list,
            "单位净值": [self.get_unit_value(date) for date in date_list],
            "累计净值": [self.get_cumulative_value(date) for date in date_list],
            "日增长率": [self.get_daily_growth_rate(date) for date in date_list],
        })
        return df


if __name__ == '__main__':
    j = FuncInfo(code=161725, name="招商中证白酒指数分级")
    j.load_net_value_info(datetime(2018, 9, 1), datetime(2019, 9, 20))
    date = "2019-09-20"
    print(j.get_unit_value(date), j.get_cumulative_value(date), j.get_daily_growth_rate(date))
    df = j.get_data_frame()
    df.to_csv("./output/fund_info/161725招商中证白酒指数分级.csv")



