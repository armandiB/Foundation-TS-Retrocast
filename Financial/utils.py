def is_float(element: any) -> bool:
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def make_cum_returns_df(df):
    df = df + 1
    df = df.cumprod()
    return df


def make_cum_returns_list(list_vals, start_val=1):
    res = []
    acc = start_val
    for val in list_vals:
        acc = acc*(1+val)
        res += [acc]
    return res


def find_closest_previous_date_series(series, date):
    return series[series.index < date].iat[-1]


def generate_fcd_idxs(fcds_list, index_list):
    fcds = []
    fcds_list_current_idx = 0
    for i, date in enumerate(index_list):
        if fcds_list_current_idx < len(fcds_list):
            current_fcd = fcds_list[fcds_list_current_idx]
        else:
            break
        if date >= current_fcd:
            fcds += [i]
            fcds_list_current_idx += 1

    return fcds
