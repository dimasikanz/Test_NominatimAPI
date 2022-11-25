from urllib.parse import urljoin
import requests


class JSONErrorException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url


    def request_custom(
        self,
        method,
        location,
        data=None,
        params=None,
        expected_status=200,
        jsonify=True,
        base_url_join=True,
    ):
        """
        Кастомный метод запроса, позволяет сразу же проверить код ответа и выполнить jsonify для тела ответа,
        также с его помощью происходит дополнение location к base_url. В случае необходимости, дополнение базового
        юрла можно отключить через параметр base_url_join, тем самым получив возможность самостоятельно прописать
        всю ручку для запроса.
        Для проверки запросов на прямой/обратный геокодинг не нужны никакие хедеры/куки, поэтому их мы не задаем.
        При необходимости, метод легко можно будет перестроить на выполнение сесионных запросов.
        """

        if base_url_join is True:
            url = urljoin(self.base_url, location)
        else:
            url = location

        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params
        )
        assert (response.status_code == expected_status), f"Expected {expected_status} status code, but got {response.status_code}"

        if jsonify:
            try:
                json_response: dict = response.json()
            except JSONErrorException:
                raise JSONErrorException(
                    f"Expected json response from api request {url}"
                )
            return json_response
        return response
