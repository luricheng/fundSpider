from fund_list import get_fund_df
from fund_info import FuncInfo
from tqdm import tqdm
import pickle

if __name__ == '__main__':
    start_date, end_date = "2000-01-01", "2019-09-21"
    fund_df = get_fund_df()
    fund_num = len(fund_df)
    print("total fund: %s" % fund_num)
    for idx in tqdm(range(fund_num)):
        row = fund_df.iloc[idx]
        info = FuncInfo(code=row.code, name=row.name, fund_type=row.type)
        info.load_net_value_info(start_date, end_date)
        with open("./output/pkl_data/%s.pkl" % row.code, 'wb') as fp:
            pickle.dump(info, fp, protocol=pickle.HIGHEST_PROTOCOL)
