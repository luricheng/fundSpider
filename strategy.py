# -*- coding: utf-8 -*-

class Strategy(object):
    @classmethod
    def bottom_suction_high_throw(cls,
                                  value_list,
                                  start_idx=0,
                                  end_idx=None,
                                  base_money=100,
                                  add_money=10,
                                  take_profit_rate=0.05):
        """
        低吸高抛策略, 一只基金从发行到现在 投入资金&回报
        :param value_list: 基金净值list
        :param start_idx: 开始投资时刻
        :param end_idx: 结束投资时刻
        :param base_money: 建仓成本
        :param add_money: 每次加仓成本
        :param take_profit_rate: 止盈率
        :return:
        """
        if len(value_list) < 2:
            raise Exception("value_list's length must > 1, but got %s" % len(value_list))
        end_idx = end_idx or len(value_list)
        end_idx = min(end_idx, len(value_list))
        total_cost = base_money                             # 总成本
        holding_share = 1.0 * base_money / value_list[start_idx]    # 持有份额
        for i in range(start_idx+1, end_idx):
            value = value_list[i]
            pre_value = value_list[i-1]
            # 跌
            if value < pre_value:
                total_cost += add_money
                holding_share += 1.0 * add_money / value
            # 涨 收益 > 止盈率
            if i + 1 == end_idx or cls._get_growth_rate(total_cost, holding_share, value) > take_profit_rate:
                return {
                    "cost_time": i-start_idx,
                    "total_cost": total_cost,
                    "profit_rate": cls._get_growth_rate(total_cost, holding_share, value),
                }

    @staticmethod
    def _get_growth_rate(cost, holding_share, value):
        cur_val = 1.0 * holding_share * value
        return (cur_val - cost) / cost


if __name__ == '__main__':
    value_list = [1.0, 1.01, 1.0125, 0.99, 0.97, 1.009, 1.029, 1.059]
    print(Strategy.bottom_suction_high_throw(value_list))
