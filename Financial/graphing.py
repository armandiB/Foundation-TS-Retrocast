import matplotlib.pyplot as plt
from matplotlib import colormaps
from utils import make_cum_returns_df, make_cum_returns_list, find_closest_previous_date_series


def plot_quantiles(index_list, prediction_cum_list, forecasted_series, quantile_bands=((0.1, 0.9), ), ylabel='Return', title='Prediction'):
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecasted_series.index, forecasted_series.values, color='black', linewidth=1, label='Series')

    for pred_nb, (index, prediction_dict) in enumerate(zip(index_list, prediction_cum_list)):
        used_quantiles = set()
        # Plot mean line
        ax.plot(index, prediction_dict['mean'], color='blueviolet', linewidth=1, label='Mean' if pred_nb == 0 else None)
        used_quantiles.add('mean')

        # Fill between quantiles to show uncertainty bands
        for i, (lq_key, hq_key) in enumerate(quantile_bands):
            ax.fill_between(index, prediction_dict[lq_key], prediction_dict[hq_key], alpha=0.2*(1 - i/len(quantile_bands)), color='blue', label=str(lq_key)+'-'+str(hq_key) if pred_nb == 0 else None)
            used_quantiles.add(lq_key)
            used_quantiles.add(hq_key)

        colormap = colormaps['hsv']
        remaining_keys = set(prediction_dict.keys()).difference(used_quantiles)
        for i, q_key in enumerate(remaining_keys):
            ax.plot(index, prediction_dict[q_key], color=colormap(i/len(remaining_keys)), linewidth=1, label=str(q_key) if pred_nb == 0 else None)

    # Formatting
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_quantiles_returns(index_list, prediction_list, forecasted_data, col_name, quantile_bands=((0.1, 0.9),), title='Prediction'):
    forecasted_data_cum = make_cum_returns_df(forecasted_data)
    prediction_cum_list = []
    for index, prediction_dict in zip(index_list, prediction_list):
        # TODO: might want to reset start point to median each day for other quantiles?
        prediction_cum_list += [{key: make_cum_returns_list(list_vals, start_val=find_closest_previous_date_series(forecasted_data_cum[col_name], index[0])) for key, list_vals in prediction_dict.items()}]
    plot_quantiles(index_list, prediction_cum_list, forecasted_data_cum, quantile_bands=quantile_bands, ylabel=col_name, title=title)
