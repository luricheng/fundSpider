from fund_list import get_fund_list
from fund_info import FuncInfo
# from tqdm import tqdm
import os
from p_tqdm import p_umap

csv_data_dir = "./output/csv_data"

def get_fund(fund):
    code = fund.get("code")
    # name = fund.get("name")
    file_name = os.path.join(csv_data_dir, u"%s.csv" % code)
    if os.path.isfile(file_name):
        return
    info = FuncInfo(code=code)
    info.load_net_value_info(start_date, end_date)
    df = info.get_data_frame()
    df.to_csv(file_name)


if __name__ == '__main__':
    start_date, end_date = "2000-01-01", "2019-09-21"
    fund_list = get_fund_list()
    fund_num = len(fund_list)
    print("total fund: %s" % fund_num)
    p_umap(get_fund, fund_list)

