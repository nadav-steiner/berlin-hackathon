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


class InputServiceInstance(ServiceInstance):
    time_ago = '5mi-ago'
    uaa = 'https://902cab2a-2aba-46ac-9457-b52e24f7b5c3.predix-uaa.run.aws-usw02-pr.ice.predix.io'
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxNDJiNWE3YWE1MTk0MzRmOWQzNjY1ZmMwZGQxN2NlMiIsInN1YiI6InVzZXIiLCJzY29wZSI6WyJ0aW1lc2VyaWVzLnpvbmVzLmQ0MGJmOGUyLThjMDYtNDlhMi1iZDA4LTE0M2Q1MTk5YzhkOC5xdWVyeSIsInVhYS5yZXNvdXJjZSIsInRpbWVzZXJpZXMuem9uZXMuZDQwYmY4ZTItOGMwNi00OWEyLWJkMDgtMTQzZDUxOTljOGQ4LmluZ2VzdCIsIm9wZW5pZCIsInVhYS5ub25lIiwidGltZXNlcmllcy56b25lcy5jYjU1NzFjOS1kMGFkLTRhMTktYTBjYy1hZGIwZmYxNmYxMzYudXNlciIsInRpbWVzZXJpZXMuem9uZXMuY2I1NTcxYzktZDBhZC00YTE5LWEwY2MtYWRiMGZmMTZmMTM2LnF1ZXJ5IiwidGltZXNlcmllcy56b25lcy5kNDBiZjhlMi04YzA2LTQ5YTItYmQwOC0xNDNkNTE5OWM4ZDgudXNlciIsInRpbWVzZXJpZXMuem9uZXMuY2I1NTcxYzktZDBhZC00YTE5LWEwY2MtYWRiMGZmMTZmMTM2LmluZ2VzdCJdLCJjbGllbnRfaWQiOiJ1c2VyIiwiY2lkIjoidXNlciIsImF6cCI6InVzZXIiLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6ImM0YzU3OWJhIiwiaWF0IjoxNDk3MjczNjE5LCJleHAiOjE0OTczMTY4MTksImlzcyI6Imh0dHBzOi8vOTAyY2FiMmEtMmFiYS00NmFjLTk0NTctYjUyZTI0ZjdiNWMzLnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiOTAyY2FiMmEtMmFiYS00NmFjLTk0NTctYjUyZTI0ZjdiNWMzIiwiYXVkIjpbInRpbWVzZXJpZXMuem9uZXMuY2I1NTcxYzktZDBhZC00YTE5LWEwY2MtYWRiMGZmMTZmMTM2IiwidWFhIiwib3BlbmlkIiwidGltZXNlcmllcy56b25lcy5kNDBiZjhlMi04YzA2LTQ5YTItYmQwOC0xNDNkNTE5OWM4ZDgiLCJ1c2VyIl19.JRnXiaQTzuvMq-DzVC9JtIsWUTA2ZN23nOE2IyVKrMJyUr47JUxYthVrJ9Ve3AgGcLZh52Y8lblztF9RS8fnM3OKHNym3wD3NLOXCEPx9VQCuvGV9WbTLaQpHomZjVYhqKSf4bBRKiULFctitC9WBsfAFktdY73RkpI-rWluhnzEEVs1Prn-e_sg7uYAYgcv_RVIJ-aiHEnYWzWTRYlqNBL5EgwXhGriraXR8xCSwadO3bj1ACFBIxVrXLQTrzYjHprcm2D-WTt_koqZuoFeDBgDq7KTcQfX7_EwxRw0KjxyyxrEDj1Zux7YoR1gMT6q56MesHcnJ9FNSpBkvYul8A'
    zone_id = 'cb5571c9-d0ad-4a19-a0cc-adb0ff16f136'
    tag = 'load_sensor'


class ESBInstance(ServiceInstance):
    time_ago = "2y-ago"
    uaa = 'https://MMEurope.predix-uaa.run.aws-usw02-pr.ice.predix.io'
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxZjdiZjIxN2U1MzM0YWNhYWJlMmNhY2RmNzQzMDIwMSIsInN1YiI6InRpbWVzZXJpZXNfY2xpZW50X3JlYWRvbmx5Iiwic2NvcGUiOlsidGltZXNlcmllcy56b25lcy4zNDY0ODk0Yy0xY2Y3LTQ0MGYtOGY1Yy1hMjczMTRlMzUwNjYucXVlcnkiLCJ0aW1lc2VyaWVzLnpvbmVzLjZlNWQ2MTUwLWYxNzItNDlmNC05ODY3LTI0ZThiNDcxMTJkYS51c2VyIiwidWFhLm5vbmUiLCJ0aW1lc2VyaWVzLnpvbmVzLjZlNWQ2MTUwLWYxNzItNDlmNC05ODY3LTI0ZThiNDcxMTJkYS5xdWVyeSIsInRpbWVzZXJpZXMuem9uZXMuMzQ2NDg5NGMtMWNmNy00NDBmLThmNWMtYTI3MzE0ZTM1MDY2LnVzZXIiXSwiY2xpZW50X2lkIjoidGltZXNlcmllc19jbGllbnRfcmVhZG9ubHkiLCJjaWQiOiJ0aW1lc2VyaWVzX2NsaWVudF9yZWFkb25seSIsImF6cCI6InRpbWVzZXJpZXNfY2xpZW50X3JlYWRvbmx5IiwiZ3JhbnRfdHlwZSI6ImNsaWVudF9jcmVkZW50aWFscyIsInJldl9zaWciOiI1OWQyYWFkOSIsImlhdCI6MTQ5NzMzNjk2MiwiZXhwIjoxNDk3MzgwMTYyLCJpc3MiOiJodHRwczovL21tZXVyb3BlLnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiNGQ4OThhMDItZjNiOS00YmNkLTlhZDktZmZmZmVjMmFkNWVmIiwiYXVkIjpbInRpbWVzZXJpZXNfY2xpZW50X3JlYWRvbmx5IiwidGltZXNlcmllcy56b25lcy4zNDY0ODk0Yy0xY2Y3LTQ0MGYtOGY1Yy1hMjczMTRlMzUwNjYiLCJ0aW1lc2VyaWVzLnpvbmVzLjZlNWQ2MTUwLWYxNzItNDlmNC05ODY3LTI0ZThiNDcxMTJkYSJdfQ.sq5HJzlh9dtf1PlajXaLN2QmrO1tG7L9DLePxwPA9Ie8JLeZ0_of3eeOTDL2bDJthI5gsknGQG2cGrr1Ztx1pVjKvH_LdMMlmneMbWevpQlkr4y191EZPQMYOSQ9lbgUxYVGh27uzr7-A5h2b5Kf7OWNyp-sNG3Q9bw5_ciDNTcbAbBvxxgfXCG0enJWmgUi83s5_vX3jUZZagG-eQoQOBWObDjgflYu-tFdquu8qJ9Knt3IzGhHmkVAI6YUZfqDPNVK94N0Ed532TSwQmZDUOu36s2-ptmSFp9936ds-qKKvPOTnxJWqDMOyLzN43F7QKUV_6P47XLvWPU8dbTMWw'
    zone_id = '3464894c-1cf7-440f-8f5c-a27314e35066'
    tag = 'LoadForecasting/LoadData/Knockroe/DC14'


class AnalyzerConfig:
    maxiter = 100
    host = '0.0.0.0'
    port = 8080
    thresh = 0.1
    sim_time_max = 10
    get_dp_n = 10000
    ws_url = 'wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages'
    data_url = 'https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints'
    tags_url = 'https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/tags'
    # input = InputServiceInstance
    inputs = InputServiceInstance, ESBInstance
    input = inputs[1]
    window_len = 300
    window_step = window_len // 10
    compute_live = False
    inject_len = window_len * 3
    inject_idx = 0
    sim_ingest = 0
    sim_data = 0
    do_compute = 1


class Quality:
    bad = 0
    uncertain = 1
    good = 3


def get_config():
    return AnalyzerConfig