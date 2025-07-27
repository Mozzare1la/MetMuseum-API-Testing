import requests as rq
from http.client import responses
import pytest
import logging


logging.basicConfig(level=logging.INFO)
url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"


@pytest.mark.parametrize("limit", [100])
def test_rate_limiting(limit):
    logging.info("Проверка ограничения на количество запросов")
    for i in range(1, limit):
        rsp: rq.Response = rq.get(url + str(i))
        if rsp.status_code == 429:
            logging.info(
                f"Ограничение количества запросов найдено: {i} /n{rsp.status_code} - {responses}"
            )
            break

    logging.warning(f"Ограничение не найдено, запросов отправлено: {limit}")
