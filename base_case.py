import pytest
from builder import Builder


class ApiBase:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, api_client):
        """
        Метод для определения api_client, а также bulder - класса для составления params к запросам
        """
        self.api_client = api_client
        self.builder = Builder()
