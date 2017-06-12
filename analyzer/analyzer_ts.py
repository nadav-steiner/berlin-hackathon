import asyncio
import logging

import aiohttp
import numpy
import time
from aiohttp import web


class Quality:
    bad = 0
    uncertain = 1
    good = 3


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(10)

ref_time = time.time()

loop = asyncio.get_event_loop()


def get_time():
    return time.time()  # - ref_time


class ServiceInstance:
    token = None
    zone_id = None

    @classmethod
    def get_auth_headers(cls):
        return {
            'authorization': 'Bearer ' + cls.token,
            'predix-zone-id': cls.zone_id,
            'Origin': 'http://localhost'
        }


class OutputServiceInstance(ServiceInstance):
    pass


class InputServiceInstance(ServiceInstance):
    time_ago = '5mi-ago'
    uaa = 'https://902cab2a-2aba-46ac-9457-b52e24f7b5c3.predix-uaa.run.aws-usw02-pr.ice.predix.io'
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxNDJiNWE3YWE1MTk0MzRmOWQzNjY1ZmMwZGQxN2NlMiIsInN1YiI6InVzZXIiLCJzY29wZSI6WyJ0aW1lc2VyaWVzLnpvbmVzLmQ0MGJmOGUyLThjMDYtNDlhMi1iZDA4LTE0M2Q1MTk5YzhkOC5xdWVyeSIsInVhYS5yZXNvdXJjZSIsInRpbWVzZXJpZXMuem9uZXMuZDQwYmY4ZTItOGMwNi00OWEyLWJkMDgtMTQzZDUxOTljOGQ4LmluZ2VzdCIsIm9wZW5pZCIsInVhYS5ub25lIiwidGltZXNlcmllcy56b25lcy5jYjU1NzFjOS1kMGFkLTRhMTktYTBjYy1hZGIwZmYxNmYxMzYudXNlciIsInRpbWVzZXJpZXMuem9uZXMuY2I1NTcxYzktZDBhZC00YTE5LWEwY2MtYWRiMGZmMTZmMTM2LnF1ZXJ5IiwidGltZXNlcmllcy56b25lcy5kNDBiZjhlMi04YzA2LTQ5YTItYmQwOC0xNDNkNTE5OWM4ZDgudXNlciIsInRpbWVzZXJpZXMuem9uZXMuY2I1NTcxYzktZDBhZC00YTE5LWEwY2MtYWRiMGZmMTZmMTM2LmluZ2VzdCJdLCJjbGllbnRfaWQiOiJ1c2VyIiwiY2lkIjoidXNlciIsImF6cCI6InVzZXIiLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6ImM0YzU3OWJhIiwiaWF0IjoxNDk3MjczNjE5LCJleHAiOjE0OTczMTY4MTksImlzcyI6Imh0dHBzOi8vOTAyY2FiMmEtMmFiYS00NmFjLTk0NTctYjUyZTI0ZjdiNWMzLnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiOTAyY2FiMmEtMmFiYS00NmFjLTk0NTctYjUyZTI0ZjdiNWMzIiwiYXVkIjpbInRpbWVzZXJpZXMuem9uZXMuY2I1NTcxYzktZDBhZC00YTE5LWEwY2MtYWRiMGZmMTZmMTM2IiwidWFhIiwib3BlbmlkIiwidGltZXNlcmllcy56b25lcy5kNDBiZjhlMi04YzA2LTQ5YTItYmQwOC0xNDNkNTE5OWM4ZDgiLCJ1c2VyIl19.JRnXiaQTzuvMq-DzVC9JtIsWUTA2ZN23nOE2IyVKrMJyUr47JUxYthVrJ9Ve3AgGcLZh52Y8lblztF9RS8fnM3OKHNym3wD3NLOXCEPx9VQCuvGV9WbTLaQpHomZjVYhqKSf4bBRKiULFctitC9WBsfAFktdY73RkpI-rWluhnzEEVs1Prn-e_sg7uYAYgcv_RVIJ-aiHEnYWzWTRYlqNBL5EgwXhGriraXR8xCSwadO3bj1ACFBIxVrXLQTrzYjHprcm2D-WTt_koqZuoFeDBgDq7KTcQfX7_EwxRw0KjxyyxrEDj1Zux7YoR1gMT6q56MesHcnJ9FNSpBkvYul8A'
    zone_id = 'cb5571c9-d0ad-4a19-a0cc-adb0ff16f136'
    tag = 'load_sensor'


class ESBInstance(ServiceInstance):
    time_ago = "1y-ago"
    uaa = 'https://MMEurope.predix-uaa.run.aws-usw02-pr.ice.predix.io'
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI4MDBiZmU1OWM1MTA0NDI4YWRmMDdhOWRhZTVlYzVlYyIsInN1YiI6InRpbWVzZXJpZXNfY2xpZW50X3JlYWRvbmx5Iiwic2NvcGUiOlsidGltZXNlcmllcy56b25lcy4zNDY0ODk0Yy0xY2Y3LTQ0MGYtOGY1Yy1hMjczMTRlMzUwNjYucXVlcnkiLCJ0aW1lc2VyaWVzLnpvbmVzLjZlNWQ2MTUwLWYxNzItNDlmNC05ODY3LTI0ZThiNDcxMTJkYS51c2VyIiwidWFhLm5vbmUiLCJ0aW1lc2VyaWVzLnpvbmVzLjZlNWQ2MTUwLWYxNzItNDlmNC05ODY3LTI0ZThiNDcxMTJkYS5xdWVyeSIsInRpbWVzZXJpZXMuem9uZXMuMzQ2NDg5NGMtMWNmNy00NDBmLThmNWMtYTI3MzE0ZTM1MDY2LnVzZXIiXSwiY2xpZW50X2lkIjoidGltZXNlcmllc19jbGllbnRfcmVhZG9ubHkiLCJjaWQiOiJ0aW1lc2VyaWVzX2NsaWVudF9yZWFkb25seSIsImF6cCI6InRpbWVzZXJpZXNfY2xpZW50X3JlYWRvbmx5IiwiZ3JhbnRfdHlwZSI6ImNsaWVudF9jcmVkZW50aWFscyIsInJldl9zaWciOiI1OWQyYWFkOSIsImlhdCI6MTQ5NzI4MDIxNywiZXhwIjoxNDk3MzIzNDE3LCJpc3MiOiJodHRwczovL21tZXVyb3BlLnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiNGQ4OThhMDItZjNiOS00YmNkLTlhZDktZmZmZmVjMmFkNWVmIiwiYXVkIjpbInRpbWVzZXJpZXNfY2xpZW50X3JlYWRvbmx5IiwidGltZXNlcmllcy56b25lcy4zNDY0ODk0Yy0xY2Y3LTQ0MGYtOGY1Yy1hMjczMTRlMzUwNjYiLCJ0aW1lc2VyaWVzLnpvbmVzLjZlNWQ2MTUwLWYxNzItNDlmNC05ODY3LTI0ZThiNDcxMTJkYSJdfQ.C0QzV5Df3hU5SIGz9qamr-idYm0rQJfhYQbQICwSUmlqYepNYJXROUWQs_uJRQL3Ny9uAEtYWXkbZ2JA451RsF6GucyAPOVmW97DFK2M70WgbNASq4RNyYzJykrM5c89SB1CXQbmXsnrHebtLZbIaDm02bZ3KUarG_-HjW1Mhi3Ork92vMOUl5jBxqqc-ZCt7Zt12AEYW5SAibAIolB4OLI5KoHnlLbNQk_6AVR9mF1upu1RMN8ScgIUW389DqpgvIQkuQIQdcz69-_32B_5z2_oCH951CKKAvyEhAqzJX-_JWS4xk_wYuAT5bpEIOcH3TSu0OKLSTWLFIsXvQ5Nhw'
    zone_id = '3464894c-1cf7-440f-8f5c-a27314e35066'
    tag = 'LoadForecasting/LoadData/Knockroe/DC14'


class AnalyzerConfig:
    thresh = 0.1
    ws_url = 'wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages'
    data_url = 'https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints'
    tags_url = 'https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/tags'
    input = InputServiceInstance
    # input = ESBInstance
    window_len = 100
    sim_ingest = 0


def get_config():
    return AnalyzerConfig


def get_time_ms_int():
    return int(time.time() * 1e3)


class Analyzer:
    def __init__(self):
        self.feeder_id = 1
        self.tag = get_config().input.tag
        self.data = []
        self.fv = [Quality.good]
        self.dq = [[0, 0]]
        self.tags = []

    async def main_async(self):
        logger.debug('reading from: %s', self.tag)
        config = get_config()
        if config.sim_ingest:
            loop.create_task(self.sim_injest())

        loop.create_task(self.start_server())
        while True:
            predix_values = await self.get_predix_data()
            if not len(predix_values):
                break
            self.data = numpy.asarray(predix_values)[:, :2]

            dq = await self.get_dq()
            logger.debug('got dq: %s', dq)

            await asyncio.sleep(.01)

    def main(self):
        asyncio.get_event_loop().run_until_complete(self.main_async())

    async def get_ts(self, request):
        debug = logger.debug
        # data = await request.json()
        # debug(data)
        res = await self.get_res()
        return web.json_response(res, headers={'Access-Control-Allow-Origin': '*'})

    async def put_rec(self, rec):
        pass

    async def sim_injest(self):
        config = get_config()

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(config.ws_url, headers=config.input.get_auth_headers()) as ws:
                while True:
                    data = [[get_time_ms_int(), numpy.random.rand(1).item(), Quality.good]]
                    data = await self.get_injest_data(data)

                    await ws.send_json(data)
                    recv = await ws.receive_json()
                    await asyncio.sleep(.1)

    async def get_injest_data(self, data):
        config = get_config()
        tms = get_time_ms_int()
        data_list = [[*row] for row in data]

        data = {
            "messageId": tms,
            "body": [
                {
                    "name": config.test_tag,
                    "datapoints": data_list
                }
            ]
        }
        return data

    async def get_res(self):
        debug = logger.debug
        data = numpy.asarray(self.data, dtype=float)
        if not len(data):
            return
        tp, xp = data.T
        t = get_time()
        # idx = data[:, 0].searchsorted(t)
        x = numpy.interp(t, tp, xp)
        # t, x = data[idx]
        dq = await self.get_dq()
        self.dq.append(dq)

        res = dict(time=t,
                   value=data[-1, 1],
                   dq=self.dq[-1],
                   fv=self.fv[-1])
        debug(res)
        return res

    async def get_dq(self):
        # data = numpy.asarray(self.data[-get_config().window_len:])
        # print(*self.data, sep='\n')
        if not len(self.data):
            return
        data = numpy.asarray(self.data)

        fv = self.arma_sm(data[:, 1])
        if fv is None:
            return Quality.uncertain

        self.fv.append(list(fv))

        if fv is None:
            return Quality.uncertain

        r = numpy.linalg.norm(fv)

        if r < get_config().thresh:
            return Quality.good
        else:
            return Quality.bad

    async def get_predix_data(self):
        values = await self.get_data_from_tag(self.tag)
        # logger.debug('appending values: %s', values)
        # logger.debug(self.data)
        # pdata = numpy.asarray(values)
        return values
        # self.data.append(values[:2])

    async def get_data_from_tag(self, tag):
        config = get_config()
        request_dict = dict(
            url=config.data_url,
            headers=config.input.get_auth_headers(),
            json={
                "start": config.input.time_ago,
                "tags": [
                    {
                        "name": tag,
                        "order": "asc",
                        "limit": config.window_len
                    }
                ]
            }
        )
        async with aiohttp.ClientSession() as session:
            async with await session.post(**request_dict) as resp:
                try:
                    resp_dict = await resp.json()
                    tag = resp_dict['tags'][0]
                    results = tag['results'][0]
                    values = results['values']
                    logger.debug('len: %s, got values: %s', len(values), values)
                    return values
                except:
                    logger.error(await resp.text())
                    return None

    async def get_tags(self):
        config = get_config()
        request_dict = dict(
            url=config.tags_url,
            headers={
                'predix-zone-id': config.zone_id,
                'authorization': config.auth
            },
            data=''
        )
        async with aiohttp.ClientSession() as session:
            request = await session.get(**request_dict)
            async with request as resp:
                logger.debug(resp.status)
                resp_dict = await resp.json()
                results = resp_dict['results']
                tag_list = results
                return tag_list

    async def get_token(self):
        url = 'https://MMEurope.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token'
        headers = {
            'Pragma': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache',
            'authorization': 'Basic dGltZXNlcmllc19jbGllbnRfcmVhZG9ubHk6c2VjcmV0'
        }
        data = r'client_id=timeseries_client_readonly\r\ngrant_type=client_credentials'

    async def sim_data(self):
        debug = logger.debug
        k = 0
        while True:
            rec = (get_time(), numpy.random.rand(1).item())
            # debug('putting %s', rec)
            self.data.append(rec)
            await asyncio.sleep(.01)

    #
    # async def compute_dq(self):
    #     while True:


    def arma_sm(self, data):
        debug = logger.debug
        from statsmodels.tsa.arima_model import ARMA
        import warnings
        warnings.filterwarnings('ignore')
        try:
            model = ARMA(data, order=(0, 2)).fit(trend='c', disp=0, transparams=False, method='mle', maxiter=10)
        except (ValueError, Exception) as err:
            # debug('ARMA Fit Error', err)
            return
        else:
            return model.maparams

    async def start_server(self):
        app = web.Application()
        app.router.add_get('/', self.get_ts)
        handler = app.make_handler()
        loop = asyncio.get_event_loop()
        try:
            server = await loop.create_server(handler, '0.0.0.0', port=8080)
        except OSError as err:
            raise RuntimeError
        else:
            await server.wait_closed()


if __name__ == '__main__':
    Analyzer().main()
