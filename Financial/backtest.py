import numpy as np
import pandas as pd
from utils import make_cum_returns_df


def build_backtest_df(index_list, prediction_list, forecasted_data, quantile_for_prediction=0.5):
    index_df = []
    values_df = []
    for index, prediction_dict in zip(index_list, prediction_list):
        first_prediction_point = index[0]
        first_prediction_value = prediction_dict[quantile_for_prediction][0]
        forward_return = forecasted_data[first_prediction_point.date()]
        index_df += [first_prediction_point]
        values_df += [[first_prediction_value, forward_return]]

    backtest_df = pd.DataFrame(values_df, index=index_df, columns=['Pred_Value', 'Fwd_Ret'])

    backtest_df['Pos_Bin'] = np.sign(backtest_df['Pred_Value'])
    backtest_df['Pos_Lin'] = backtest_df['Pred_Value']

    backtest_df['Strat_Bin_Ret'] = backtest_df['Pos_Bin']*backtest_df['Fwd_Ret']
    backtest_df['Strat_Bin_CumPnl'] = backtest_df['Strat_Bin_Ret'].cumsum()

    return backtest_df
