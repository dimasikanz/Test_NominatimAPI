import pytest

import constants
from apiclient import ApiClient


def pytest_addoption(parser):
    """Чтение из консоли параметра --url, в случае, если параметр не
    указан - задает его как constants.DEFAULT_URL"""
    parser.addoption("--url", default=constants.DEFAULT_URL)


@pytest.fixture(scope="session")
def config(request):
    """
    Сессионное задание параметров конфига (в данный момент это только config['url']
    """
    url = request.config.getoption("--url")

    return {
        "url": url
    }


@pytest.fixture(scope="session")
def api_client(config):
    """
    Возврат класса ApiClient
    """
    return ApiClient(
        base_url=config["url"]
    )
