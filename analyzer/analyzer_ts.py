import asyncio
import logging
import numpy
import time
from aiohttp import web

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(10)
ref_time = time.time()


def get_time():
    return time.time() - ref_time

class AnalyzerConfig:
    window_len = 200


def get_config():
    return AnalyzerConfig


class Analyzer:
    def __init__(self):
        self.data = []
        self.fv = []
        self.dq = []

    def main(self):
        asyncio.get_event_loop().run_until_complete(self.main_async())

    async def get_ts(self, request):
        debug = logger.debug
        # data = await request.json()
        # debug(data)
        res = await self.get_res()
        return web.json_response(res)

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
        data = numpy.asarray(self.data[-get_config().window_len:])
        fv = self.arma_sm(data[:, 1])
        self.fv.append(list(fv))
        if fv is None:
            return 1

        r = numpy.linalg.norm(fv)
        if r < .1:
            return 0
        else:
            return 1

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
        except ValueError as err:
            debug('ARMA Fit Error', err)
            return
        else:
            return model.maparams

    async def main_async(self):
        asyncio.get_event_loop().create_task(self.sim_data())
        # while True:
        #     await self.get_res()
        #     await asyncio.sleep(.5)
        await self.start_server()

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
