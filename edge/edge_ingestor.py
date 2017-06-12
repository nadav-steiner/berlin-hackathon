#!/usr/bin/env python3

from websocket import create_connection
import os
import logging
import json
import time
import random
import subprocess
import sys

PIDSTR = str(os.getpid())
INGEST_URL = 'wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages'

IS_BUTTON_PRESSED_FILE = "is_button_pressed"
TOKEN_CURL_CMD = r"curl 'https://902cab2a-2aba-46ac-9457-b52e24f7b5c3.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token' -H 'Pragma: no-cache' -H 'content-type: application/x-www-form-urlencoded' -H 'Cache-Control: no-cache' -H 'authorization: Basic dXNlcjpzZWNyZXQ=' --data 'client_id=user&grant_type=client_credentials'"
PREDIX_ZONE_ID = "cb5571c9-d0ad-4a19-a0cc-adb0ff16f136"
LOAD_DATA_FILE = "GE JOD L4 Set.csv"

SENSOR_ID = "load_sensor"

logging.basicConfig(level=logging.INFO)

def get_token():
    output = subprocess.check_output(TOKEN_CURL_CMD, shell=True, stderr=subprocess.DEVNULL)
    output_str = output.decode()
    outpot_json = json.loads(output_str)
    return str(outpot_json['access_token'])


def get_message_id():
    return PIDSTR + str(int(round(1000*time.time())))


def ts_to_predix_ts(ts):
    return int(round(1000*ts))


def create_ingest_body(sensor_id, datapoints_arr):
    mid = get_message_id()

    return {'messageId': mid,
            'body': [{
                "name": str(sensor_id),
                "datapoints": datapoints_arr,
            }]}


def get_data_generator():
    with open(LOAD_DATA_FILE) as f:
        count = 0
        for line in f:
            if count < 8:
                count += 1
                continue
            value = line.split()[1].split(',')[1]
            yield float(value)


def get_next_value(is_button_pressed, data_generator):
    if is_button_pressed:
        return 0  # random.uniform(40, 96)
    else:
        return next(data_generator)


def ingest(predix_zone_id, token, data_generator, num_datapoints_per_msg):
    logging.info("started ingest")

    with open(IS_BUTTON_PRESSED_FILE) as f:
        is_button_pressed = int(f.read())

    headers = {'Predix-Zone-Id': predix_zone_id,
               'Authorization': 'Bearer ' + token,
               'Origin': 'http://localhost/'}

    ws = create_connection(INGEST_URL, header=headers)

    datapoints_arr = [[ts_to_predix_ts(time.time()), get_next_value(is_button_pressed, data_generator)] for i
                      in range(num_datapoints_per_msg)]
    ws.send(json.dumps(create_ingest_body(SENSOR_ID, datapoints_arr)))
    for datapoint in datapoints_arr:
        logging.info("sent ts=%s, value=%s" % (str(datapoint[0]), str(datapoint[1])))

    result = ws.recv()
    logging.info("ingestion result %s" % result)


def main():
    logging.info("edge ingestor started")

    sleep_time = float(sys.argv[1])
    num_datapoints_per_msg = int(sys.argv[2])

    token = get_token()

    data_generator = get_data_generator()

    while True:
        ingest(PREDIX_ZONE_ID, token, data_generator, num_datapoints_per_msg)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
