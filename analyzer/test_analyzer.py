import pytest

from predix_wrap import PredixWrap


def test_get_token():
    token = PredixWrap().get_token()
    print(token)