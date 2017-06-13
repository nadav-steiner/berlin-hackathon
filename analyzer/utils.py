import asyncio
import logging
import time

logging.basicConfig()
ref_time = time.time()


def get_time():
    return time.time() - ref_time


def get_time_ms_int():
    return int(time.time() * 1e3)