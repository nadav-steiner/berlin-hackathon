#!/usr/bin/env python3

from websocket import create_connection
from collections import namedtuple
import os
import logging
import json
import time
import requests
import argparse
s

class TimeSeriesTransport:
    INGEST_URL = 'wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages'
    QUERY_URL='https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints'

    def __init__(self, predix_zone_id, user_token_file):
        self._predix_zone_id = predix_zone_id
        self._user_token_file = user_token_file

        with open(self._user_token_file) as f:
            self._user_token = f.read()

    def _get_headers(self):
        with open(self._user_token_file) as f:
            headers = {'Predix-Zone-Id': self._predix_zone_id,
                       'Authorization': 'Bearer ' + self._user_token,
                       'Content-Type': 'application/json'}
        return headers


def ts_to_predix_ts(ts):
    return int(round(1000 * ts))


DataPoint = namedtuple("DataPoint", ["timestamp", "measure", "quality"])


class IngestMessage:

    def __init__(self, tag, datapoint_arr, **attrs):
        assert isinstance(datapoint_arr, list) or isinstance(datapoint_arr, DataPoint)
        self._tag = tag
        self._datapoint_arr = datapoint_arr
        self._attrs = attrs


class TimeSeriesIngest:
    _pidstr = str(os.getpid())

    def __init__(self, predix_zone_id, user_token_file):
        self._transporter = TimeSeriesTransport(predix_zone_id, user_token_file)

    @staticmethod
    def _get_message_id():
        return TimeSeriesIngest._pidstr + str(int(round(1000 * time.time())))

    def _get_datapoints_string():

    @staticmethod
    def _get_ingest_body(ingest_msg):
        mid = TimeSeriesIngest._get_message_id()
        datapoints = [[ts_to_predix_ts(ts), measure, quality] for (ts, measure, quality) in ingest_msg.datapoint_arr ]
        return {'messageId': mid,
                'body': [{
                    "name": str(ingest_msg.sensor_id),
                    "datapoints": datapoints,
                    "attributes": ingest_msg.attrs
                }]}

    def ingest(self, ingest_msg):
        assert isinstance(ingest_msg)
        ingest_body_str = self._get_ingest_body(ingest_msg)


class TimeSeriesQuery:
    def __init__(self, predix_zone_id, user_token_file):
        self._transporter = TimeSeriesTransport(predix_zone_id, user_token_file)

    @staticmethod
    def _create_query_body(sensor_id, start_time, end_time):
        return {
            "cache_time": 0,
            "tags": [
                {
                    "name": sensor_id,
                    "order": "asc"
                }
            ],
            "start": ts_to_predix_ts(start_time),
            "end": ts_to_predix_ts(end_time)
        }

