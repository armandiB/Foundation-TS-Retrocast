import datetime as dt
import sys
from data import import_csv_data, df_to_series_dict
from api import request_forecast, process_response, collect_results
from graphing import plot_quantiles_returns
from utils import generate_fcd_idxs


if __name__ == "__main__":
    snp_data_file = 'SPX Daily returns 2016-2024.csv'
    model = 'tabpfn-ts'  # 'chronos-bolt'  # 'tabpfn-ts', 'chronos-2'
    col_name = 'Return'
    batch_request = True
    wait_for_results = True
    known_job_id = None

    snp_data = import_csv_data(snp_data_file, date_format="%m/%d/%y", col_name=col_name)
    prepared_data_dict = df_to_series_dict(snp_data, col_name=col_name)

    payload = {
        "series": [prepared_data_dict],
        "horizon": 1,
        "freq": "D",
        "context": None,
        "quantiles": [0.1, 0.9, 0.3, 0.7, 0.5],
    }

    fcds_list = sorted([dt.date(year, month, 1).strftime("%Y-%m-%d") for year in range(2017, 2025) for month in range(1, 13)])
    payload["series"][0]["fcds"] = generate_fcd_idxs(fcds_list, prepared_data_dict['index'])
    # payload["series"][0]["fcds"] = list(range(1, len(prepared_data_dict['index'])))

    if known_job_id is None or not batch_request:
        forecast_response = request_forecast(payload, model=model, batch=batch_request)
    else:
        forecast_response = None

    response_json = collect_results(forecast_response, batch=batch_request, wait_for_results=wait_for_results, known_job_id=known_job_id)

    if ("status" in response_json.keys() and response_json["status"] == "in_progress") or "series" not in response_json.keys():
        print(response_json)
        sys.exit(1)

    print(response_json)
    index_list, prediction_list, metrics_list = process_response(response_json)

    print(metrics_list)
    plot_quantiles_returns(index_list, prediction_list, snp_data, col_name, quantile_bands=((0.1, 0.9),), title='Prediction')
