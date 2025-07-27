import requests as rq
from http.client import responses
from pydantic import ValidationError
import pytest
import logging
import time

from models import SearchResults


logging.basicConfig(level=logging.INFO)
url = "https://collectionapi.metmuseum.org/public/collection/v1/search"


def get_object_by_id(obj_id: int):
    rsp = rq.get(
        f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
    )
    rsp.raise_for_status()
    return rsp.json()


def kwd_in_tags(kwd: str, tags: list[dict]) -> bool:
    if tags != None:
        for d in tags:
            if d["term"].lower() == kwd.lower():
                return True
    return False


@pytest.mark.parametrize("kwd", ["sunflowers"])
def test_search(kwd):
    logging.info(f"Проверка поиска элементов по параметрам")
    logging.info(f"Запрос к {url}?q={kwd}&tags=true")

    try:
        rsp = rq.get(url, params={"tags": "true", "q": kwd})
        rsp.raise_for_status()
    except rq.exceptions.HTTPError as err:
        logging.error(
            f"Ошибка! Статус запроса {rsp.status_code} - {responses[rsp.status_code]}"
        )
        raise err

    try:
        search_results = SearchResults.model_validate_json(rsp.text)
    except ValidationError as err:
        logging.error(f"Полученные данные не соответствуют модели")
        raise err

    assert search_results.total > 0, f"Поиск по {kwd} не вернул результатов"
    logging.info(f"Найдено объектов {search_results.total}: {search_results.objectIDs}")

    objects_cant_test = 0
    objects_not_kwd_in = 0

    for id in search_results.objectIDs:
        # Время между запросами (для избежания ошибки 403)
        time.sleep(0.5)

        try:
            json_response = get_object_by_id(id)
        except Exception as e:
            logging.warning(f"Не удалось проверить объект c ID={id}\n{str(e)}")
            objects_cant_test += 1
            continue

        if not kwd_in_tags(kwd, json_response["tags"]):
            logging.error(f"У объекта с ID={id} не найдено ключевое слово {kwd}")
            objects_not_kwd_in += 1

    assert (
        objects_not_kwd_in == 0
    ), f"Ключевое слово {kwd} отсутствует tags в у {objects_not_kwd_in} объектов"

    if objects_cant_test != 0:
        logging.warning(f"Не удалось проверить объектов: {objects_cant_test}")
