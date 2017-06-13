import asyncio

import aiohttp
import logging
import numpy

from analyzer.config import get_config, Quality

logger = logging.getLogger().getChild('wrap')

class PredixWrap:
    config = get_config()

    def __init__(self, tag=None):
        self.tag = tag or self.config.input.tag
        logger.debug('tag name: %s', self.tag)

    async def get_datapoints(self, n):
        request_dict = dict(
            url=self.config.data_url,
            headers=self.config.input.get_auth_headers(),
            json={
                "start": self.config.input.time_ago,
                "tags": [
                    {
                        "name": self.tag,
                        "order": "asc",
                        "limit": n
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
                    logger.debug('len: %s, got values: %s ...', len(values), values[:5])
                except Exception as err:
                    logger.error(await resp.text())
                    raise ValueError(err)
                else:
                    return values

    async def sim_ingest(self, data):
        config = self.config

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(config.ws_url, headers=config.input.get_auth_headers()) as ws:
                while True:
                    data = [[get_time_ms_int(), numpy.random.rand(1).item(), Quality.good]]
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

                    await ws.send_json(data)
                    # recv = await ws.receive_json()
                    # await asyncio.sleep(.1)

    async def get_tags(self):
        config = get_config()
        request_dict = dict(
            url=config.tags_url,
            headers={
                'predix-zone-id': config.zone_id,
                'authorization': config.auth
            }
        )

        async with aiohttp.ClientSession() as session:
            async with await session.get(**request_dict) as resp:
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
