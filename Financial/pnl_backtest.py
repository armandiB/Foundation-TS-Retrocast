import numpy as np
import pandas as pd
from utils import find_closest_next_or_equal_index


def build_backtest_df(index_list, prediction_list, forecasted_returns, quantile_for_prediction=0.5):
    index_df = []
    values_df = []
    print(forecasted_returns['2024-01-01':].index)
    for index, prediction_dict in zip(index_list, prediction_list):
        first_prediction_point = index[0]
        first_prediction_value = prediction_dict[quantile_for_prediction][0]
        forward_return = forecasted_returns[find_closest_next_or_equal_index(forecasted_returns, first_prediction_point.strftime("%Y-%m-%d"))]
        index_df += [first_prediction_point]
        values_df += [[first_prediction_value, forward_return]]

    backtest_df = pd.DataFrame(values_df, index=index_df, columns=['Pred_Value', 'Fwd_Ret'])

    backtest_df['Pos_Bin'] = np.sign(backtest_df['Pred_Value'])
    backtest_df['Pos_Lin'] = backtest_df['Pred_Value']

    ## Final pnls for strategies
    # TODO: temporary

    backtest_df['Strat_Long_CumPnl'] = backtest_df['Fwd_Ret'].cumsum() / backtest_df['Fwd_Ret'].std()

    backtest_df['Strat_Bin_Ret'] = backtest_df['Pos_Bin']*backtest_df['Fwd_Ret']
    backtest_df['Strat_Bin_CumPnl'] = backtest_df['Strat_Bin_Ret'].cumsum() / backtest_df['Strat_Bin_Ret'].std()

    backtest_df['Strat_Lin_Ret'] = backtest_df['Pos_Lin']*backtest_df['Fwd_Ret']
    backtest_df['Strat_Lin_CumPnl'] = backtest_df['Strat_Lin_Ret'].cumsum() / backtest_df['Strat_Lin_Ret'].std()

    return backtest_df
