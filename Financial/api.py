import requests
import datetime as dt
import time
from urllib.parse import urljoin
from utils import is_float

RETROCAST_URL = "https://api.retrocast.com"
API_KEY = ""


def request_forecast(payload, model='tabpfn-ts', batch=True):
    url = urljoin(RETROCAST_URL, "forecast" + ("-jobs" if batch else "") + "?model=" + model)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def request_batch_results(job_id):
    url = urljoin(RETROCAST_URL, "forecast-jobs/" + job_id)
    headers = {"Authorization": "Bearer " + API_KEY}
    response = requests.get(url, headers=headers)
    return response


def collect_results(forecast_response, batch=True, wait_for_results=True, known_job_id=None):
    if batch:
        job_id = known_job_id if known_job_id is not None else forecast_response.text[1:-1]
        print(job_id)
        response_json = request_batch_results(job_id).json()
        if wait_for_results:
            while "status" in response_json.keys() and response_json["status"] == "in_progress":
                print("Waiting... " + dt.datetime.now().ctime())
                time.sleep(30)
                response_json = request_batch_results(job_id).json()
    else:
        response_json = forecast_response.json()

    return response_json


def process_response(response_json):
    index_list = []
    prediction_list = []
    metrics_list = []
    for results_prediction in response_json['series'][0]:
        index_temp = results_prediction['index']
        index = [dt.datetime.strptime(st, '%Y-%m-%dT%H:%M:%S') for st in index_temp]
        metrics = results_prediction['metrics']
        prediction_dict_temp = results_prediction['prediction']
        prediction_dict = {float(key) if is_float(key) else key: val for key, val in prediction_dict_temp.items()}
        index_list += [index]
        prediction_list += [prediction_dict]
        metrics_list += [metrics]
    return index_list, prediction_list, metrics_list


def request_api_spec():
    url = "https://api.retrocast.com/openapi"
    response = requests.get(url)
    print(response.text)
    return response


if __name__ == "__main__":
    pass
