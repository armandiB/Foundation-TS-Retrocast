import os
import pandas as pd

DATA_FOLDER = r'Data'


def import_csv_data(file_name, date_format="%m/%d/%y", col_name='Return'):
    data = pd.read_csv(os.path.join(DATA_FOLDER, file_name), delimiter=',', header=None, index_col=0, parse_dates=True, date_format=date_format)
    data.columns = [col_name]
    data.index.rename('Date', inplace=True)
    data.sort_index(inplace=True)
    return data


def df_to_series_dict(df, col_name='Return'):
    return {'index': [d.strftime("%Y-%m-%d") for d in df.index.to_list()], 'target': df[col_name].to_list()}


if __name__ == "__main__":
    snp_data_file = 'SPX Daily returns 2016-2024.csv'
    snp_data = import_csv_data(snp_data_file, date_format="%m/%d/%y", col_name='Return')
    snp_data_dict = df_to_series_dict(snp_data, col_name='Return')
    print(snp_data_dict)
