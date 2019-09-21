# fundSpider
爬取天天基金数据

## 获取全量基金信息(基金代码、基金名、类型...)
截止2019-09-21 共有8966只基金

```python
import fund_list
fund_list.get_fund_df()
```

## 获取基金指定日期内单位净值、累计净值、日增长率等
```python
import fund_info
from datetime import datetime
# 招商中证白酒指数分级
info = fund_info.FuncInfo(code=161725)
# 爬取9.1~9.20的涨跌信息
info.load_net_value_info(datetime(2018, 9, 1), datetime(2019, 9, 20))
# 9.20的单位净值、累计净值、日增长率
date = "2019-09-20"
info.get_unit_value(date)
info.get_cumulative_value(date)
info.get_daily_growth_rate(date)
```

## 爬取所有基金以及相应单位净值、累计净值、日增长率等
FundInfo持久化在output/pkl_data目录下

默认2000-01-01~2019-09-20
```shell
python main.py
```