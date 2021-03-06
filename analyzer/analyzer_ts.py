import asyncio
import aiohttp
import click
import logging

import pandas
import time
from statsmodels.tsa.arima_model import ARMA
import warnings
import numpy
from aiohttp import web

from config import Quality, get_config
from predix_wrap import PredixWrap
from utils import get_time, get_time_ms_int

logger = logging.getLogger().getChild('analyzer')
logging.getLogger().setLevel(logging.DEBUG)
loop = asyncio.get_event_loop()

warnings.filterwarnings('ignore')


class Analyzer(PredixWrap):
    config = get_config()
    data = None

    def __init__(self):
        super().__init__()
        self.request_index = 0
        self.index = self.config.view_index_start
        self.last_fv = [1, 1]

    async def main_async(self):
        if not self.config.compute_live:
            await self.load_data()
            await self.insert_bad_data()
            await self.compute_dq()
            await self.show()
        logger.debug('starting server')
        await self.start_server()

    async def show(self):
        df = pandas.DataFrame(self.data)
        for k in numpy.linspace(0, self.config.sim_time_max, 20):
            print(await self.get_vals(k))
        print(df.describe())

    def get_dq(self, fv):
        if fv is None:
            return Quality.uncertain

        feature_radius = numpy.linalg.norm(fv)

        if feature_radius < self.config.thresh:
            return Quality.bad
        else:
            return Quality.good

    def get_feature_vector(self, data):
        try:
            model = ARMA(data, order=(0, 2)).fit(trend='c', disp=0, transparams=True,
                                                 maxiter=self.config.maxiter)
        except Exception as err:
            raise ValueError(err)
        else:
            return model.maparams

    async def get_vals(self, t):
        if self.config.compute_live:
            return await self.get_vals_live(t)

        tv = self.data[:, 0]
        i = self.index
        # i = tv.searchsorted(t).item()
        # if i >= len(tv):
        #     i = -1
        cols = self.data[i]

        value = cols[1]
        fv = [*cols[2: 4]]
        logger.debug('got vals: %s', (t, value, fv))
        res = dict(time=time.time(), value=value, fv=fv, dq=self.get_dq(fv))

        self.index += self.config.skip_step
        if self.index >= len(tv):
            self.index = 0
        return res

    async def start_server(self):
        app = web.Application()

        async def root(request):
            return web.json_response(
                await self.get_vals(t=get_time()),
                headers={'Access-Control-Allow-Origin': '*'})

        app.router.add_get('/', root)
        handler = app.make_handler()
        server = await loop.create_server(handler, self.config.host, port=self.config.port)
        await server.wait_closed()

    async def load_data(self, t0=get_time()):
        if self.config.sim_data:
            N = self.config.get_dp_n
            v = numpy.random.randn(N).cumsum()
        else:
            v = await self.get_values_from_predix(self.config.get_dp_n)
            N = len(v)

        self.data = numpy.c_[numpy.linspace(0, self.config.sim_time_max, N),
                             v,
                             numpy.ones((N, 2))]
        # print(self.data)

    async def get_values_from_predix(self, n):
        if self.config.sim_data:
            return numpy.random.rand(n)
        values = await self.get_datapoints(n=n)
        values = numpy.asarray(values)
        v = values[:, 1]
        return v

    def get_inject_idx(self):
        return self.config.inject_idx

    async def insert_bad_data(self):
        N = self.config.inject_len
        i = self.get_inject_idx()
        di = self.config.delta_inject
        def inject(i):
            vals = self.data[i: i + N, 1]
            nf = len(vals)
            self.data[i: i + N, 1] = vals.mean() + numpy.random.randn(nf) * vals.std()
        inject(i)
        inject(i + di)

    async def compute_dq(self):
        k = self.config.window_len
        N = len(self.data)
        kd = self.config.window_step
        fv = [1, 1]
        for i in range(k, N, kd):
            sl = slice(i - k, i)
            dw = self.data[sl, 1]
            try:
                fv = self.get_feature_vector(dw)
            except ValueError:
                pass
            else:
                dq = self.get_dq(fv)
                logger.debug('computed features: idx=%s, fv=%s, dq=%s', i, fv, dq)
            nf = len(self.data[i - kd: i, 2: 4])
            arr = numpy.asarray([fv] * nf)

            # fill out all the missing
            self.data[i - kd: i, 2: 4] = arr

    async def get_vals_live(self, t):
        try:
            v = await self.get_values_from_predix(self.config.window_len)
        except:
            return dict(time=time.time(), value=-1, fv=[1,1], dq=1)
        logger.debug('got %s values' % len(v))
        value = v[-1]
        print(v)
        # if self.request_index % 100 == 0

        try:
            fv = self.get_feature_vector(v)
        except ValueError:
            fv = [1, 1]
        # else:
        #     fv = self.last_fv
        dq = self.get_dq(fv)


        fv = [*fv]
        res = dict(time=time.time(), value=value.item(), fv=fv, dq=dq)
        print(res)
        self.request_index +=1
        return res


@click.command()
@click.option('-p', '--port', default=None, envvar='PORT')
@click.option('-d', '--original', is_flag=True, default=False)
def entry(port, original):

    config = get_config()
    config.input = config.inputs[original]
    if original:
        config.compute_live = 0
    else:
        config.port = 8081
    if port is not None:
        config.port = port
    logger.debug('port: %s', config.port)
    loop.run_until_complete(Analyzer().main_async())

if __name__ == '__main__':
    entry()
