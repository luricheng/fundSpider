import requests
import json
import pandas as pd
import numpy as np


fund_list_url = "http://fund.eastmoney.com/js/fundcode_search.js"


def fund_list_str2fmt_data(raw_str):
    """
    :param raw_str: "var r = [["000001","HXCZHH","华夏成长混合","混合型","HUAXIACHENGZHANGHUNHE"],["000002","HXCZHH","华夏成长混合(后端)","混合型","HUAXIACHENGZHANGHUNHE"]];"
    :return: [
        ["000001","HXCZHH","华夏成长混合","混合型","HUAXIACHENGZHANGHUNHE"],
        ["000002","HXCZHH","华夏成长混合(后端)","混合型","HUAXIACHENGZHANGHUNHE"]
    ]
    """
    prefix = "var r = "
    suffix = ";"
    json_str = raw_str[len(prefix): len(raw_str) - len(suffix)]
    fmt_data = json.loads(json_str)
    return fmt_data


def fund_list2dict_list(fund_list):
    dict_list = []
    for fund in fund_list:
        dict_list.append({
            "code": fund[0],
            "name_short": fund[1],
            "name": fund[2],
            "type": fund[3],
        })
    return dict_list


def fund_list2data_frame(fund_list):
    """
    :param fund_list: [
        ["000001","HXCZHH","华夏成长混合","混合型","HUAXIACHENGZHANGHUNHE"],
        ["000002","HXCZHH","华夏成长混合(后端)","混合型","HUAXIACHENGZHANGHUNHE"]
    ]
    :return:
             code        name  type  name_short
    0  000001      华夏成长混合   混合型      HXCZHH
    1  000002  华夏成长混合(后端)   混合型      HXCZHH
    """
    np_array = np.array(fund_list)
    np_array = np_array.transpose()
    df = pd.DataFrame({
        "code": np_array[0],
        "name_short": np_array[1],
        "name": np_array[2],
        "type": np_array[3]
    }, columns=["code", "name", "type", "name_short"])
    return df


def _get_fund_list():
    r = requests.get(fund_list_url)
    raw_fund_list = r.content.decode("utf-8")
    with open("./output/fund_list/raw.txt", "w") as fp:
        fp.write(raw_fund_list)
    print("get fund raw list: %s..." % raw_fund_list[:100])
    fund_list = fund_list_str2fmt_data(raw_fund_list)
    return fund_list


def get_fund_df():
    """
    获取基金表单
    :return: dataFrame
    """
    fund_df = fund_list2data_frame(_get_fund_list())
    fund_df.to_csv("./output/fund_list/fund_list.csv")
    print("parse raw data to data frame success, df head:")
    print(fund_df.head())
    return fund_df


def get_fund_list():
    dict_list = fund_list2dict_list(_get_fund_list())
    return dict_list


if __name__ == '__main__':
    get_fund_df()
