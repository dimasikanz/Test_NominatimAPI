import pytest

import apis
import constants
from builder import Builder


class ApiBase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, api_client):
        """
        Метод для определения api_client, а также bulder - класса для составления params к запросам
        """
        self.api_client = api_client
        self.builder = Builder()

    def search_address_or_name(self, params):
        lat_lon = self.api_client.request_custom(
            method="GET", location=apis.SEARCH_API_LOCATION, params=params
        )
        return lat_lon

    def reverse_lat_and_lon(self, params):
        address = self.api_client.request_custom(
            method="GET", location=apis.REVERSE_API_LOCATION, params=params
        )
        return address

    def assert_display_name_from_response(self, response, expected_words):
        display_name = response["display_name"]
        expected_words_in_display_name = True
        for word in expected_words:
            if word not in display_name:
                expected_words_in_display_name = False
                break
        assert (
            expected_words_in_display_name
        ), f"Expected {expected_words} in display_name, got {display_name}"

    def assert_lat_and_lon(self, valid_lat, valid_lon, lat, lon):
        assert (
            valid_lat in lat and valid_lon in lon
        ), f"Wrong latitude/longitude, expected in {valid_lat, valid_lon}, got {lat, lon}"

    def assert_response_is_empty_list(self, response):
        assert response == [], f"Wrong response, expected empty list, got {response}"

    def assert_error_in_response(self, response):
        assert (
            constants.ERROR_MESSAGE in response
        ), f"Unexpected response, expected {constants.ERROR_MESSAGE}, got place_data"
