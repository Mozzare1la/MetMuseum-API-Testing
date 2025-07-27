import requests as rq
from http.client import responses
from pydantic import ValidationError
import pytest
import logging

from models import Item


logging.basicConfig(level=logging.INFO)
url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"


@pytest.mark.parametrize("obj_id", [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_status_code(obj_id):
    logging.info(f"Проверка статуса кода")
    logging.info(f"Запрос к {url}{obj_id}")
    rsp = rq.get(url + str(obj_id))
    code = rsp.status_code
    assert code in responses.keys(), logging.error(f"Некорректрый код ответа - {code}")
    if code == 200:
        logging.info(f"Код ответа {code} - {responses[code]}")
    else:
        logging.warning(f"Код ответа {code} - {responses[code]}")


@pytest.mark.parametrize("obj_id", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_model_valid(obj_id):
    logging.info(f"Проверка соответствия модели")
    logging.info(f"Запрос к {url}{obj_id}")
    try:
        rsp: rq.Response = rq.get(url + str(obj_id))
        rsp.raise_for_status()
    except rq.exceptions.HTTPError as err:
        logging.error(
            f"Ошибка! Статус запроса {rsp.status_code} - {responses[rsp.status_code]}"
        )
        raise err

    try:
        assert Item.model_validate_json(rsp.text)
        logging.info(f"Объект соответствует модели")
    except ValidationError as err:
        logging.error(f"Объект {obj_id} не соответсвуется модели\n{err}")
        raise err


@pytest.mark.parametrize("obj_id", [-1])
def test_notexisting_object(obj_id):
    logging.info(f"Проверка запроса несуществующего элемента")
    logging.info(f"Запрос к {url}{obj_id}")
    try:
        rsp: rq.Response = rq.get(url + str(obj_id))
        assert rsp.status_code == 404
        logging.warning(f"Статус ответа для {url}{obj_id}: 404 - {responses[404]}")
    except AssertionError as err:
        logging.error(
            f"Ошибка! Статус запроса {rsp.status_code} - {responses[rsp.status_code]}"
        )
        raise err
