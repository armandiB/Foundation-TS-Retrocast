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
    backtest_df['Pos_BinCentered'] = np.sign(backtest_df['Pred_Value'] - backtest_df['Pred_Value'].ewm(halflife=30).mean())
    backtest_df['Pos_Lin'] = backtest_df['Pred_Value']
    backtest_df['Pos_LinCentered'] = backtest_df['Pred_Value'] - backtest_df['Pred_Value'].ewm(halflife=30).mean()

    ## Final pnls for strategies
    backtest_df['Strat_Long_NormCumPnl'] = make_norm_cum_pnl(backtest_df['Fwd_Ret'])
    for strategy_name in ['Bin', 'BinCentered', 'Lin', 'LinCentered']:
        add_backtest_for_strategy(backtest_df, strategy_name, fwd_return_col_name='Fwd_Ret')

    return backtest_df


def make_norm_cum_pnl(daily_pnl_series):
    return daily_pnl_series.cumsum() / daily_pnl_series.std()


def add_backtest_for_strategy(df, strategy_name, fwd_return_col_name='Fwd_Ret'):
    strategy_return_col_name = 'Strat_'+strategy_name+'_Ret'
    df[strategy_return_col_name] = df['Pos_'+strategy_name] * df[fwd_return_col_name]
    df['Strat_'+strategy_name+'_NormCumPnl'] = make_norm_cum_pnl(df[strategy_return_col_name])
