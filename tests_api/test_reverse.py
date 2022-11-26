import pytest

import apis
import constants
from base_case import ApiBase


@pytest.mark.API
class TestReverse(ApiBase):
    """
    Тесты для структурированного поиска по адресу (Вкладка Search -> Sctructured)
    """

    parametrize_reverse_data = [
        {"lat": "55.7514", "lon": "37.6181", "name": "Московский Кремль"},
        {"lat": "48.8582", "lon": "2.2944", "name": "Tour Eiffel"},
        {"lat": "51.48", "lon": "-0.124", "name": "Big Ben"},
        {"lat": "48.861", "lon": "2.338", "name": "Louvre"},
    ]

    @pytest.mark.parametrize("valid_place_data", parametrize_reverse_data)
    def test_reverse_parametrized(self, valid_place_data):
        """
        Параметризованный тест на определение адреса по точке. Данный тест проверяет адрес/название места, находящегося в определённой
        точке. Соответственно проверка легко может оказаться неактуальной всвязи с закрытием заведения/изменением названия улицы.
        Всвязи с этим тестовыми точками взяты известные места, название/адрес которых вряд ли поменяется.
        Кроме названия места проверяет, как дополнилась широта и долгота (в ответе на запрос эти параметры немного меняются,
        чтобы подобрать ближайший к точке адрес)
        """
        params = self.builder.reverse(
            lat=valid_place_data["lat"], lon=valid_place_data["lon"]
        ).params_for_api
        place_data = self.reverse_lat_and_lon(params=params)
        lat = place_data["lat"]
        lon = place_data["lon"]
        assert (
            valid_place_data["lat"] in lat and valid_place_data["lon"] in lon
        ), f"Wrong latitude/longitude, expected {valid_place_data['lat'], valid_place_data['lon']}, got {lat, lon}"
        self.assert_display_name_from_response(
            response=place_data, expected_words=valid_place_data["name"]
        )

    def test_space_in_lat_and_lon(self):
        """
        Тест на запрос, где широта и долгота в котором - пробелы
        Должен возвращать ошибку 400 с текстом ошибки в теле
        """
        params = self.builder.reverse(lat=" ", lon=" ").params_for_api
        place_data = self.api_client.request_custom(
            method="GET",
            location=apis.REVERSE_API_LOCATION,
            params=params,
            expected_status=400,
        )
        self.assert_error_in_response(response=place_data)

    def test_word_in_lat_and_lon(self):
        """
        Тест на запрос, с буквами в широте и долготе
        Должен возвращать ошибку 400 с текстом ошибки в теле
        """
        params = self.builder.reverse(lat="aaa", lon="bbb").params_for_api
        place_data = self.api_client.request_custom(
            method="GET",
            location=apis.REVERSE_API_LOCATION,
            params=params,
            expected_status=400,
        )
        self.assert_error_in_response(response=place_data)

    def test_no_address_at_lat_and_lon(self):
        """
        Тест на запрос, где по указанным широте и долготе нет никакого адреса/места.
        Возвращает код 200, однако в теле пишет сообщение об ошибке "Unable to geocode"
        """
        params = self.builder.reverse(
            lat=constants.NO_ADDRESS_LAT, lon=constants.NO_ADDRESS_LON
        ).params_for_api
        place_data = self.reverse_lat_and_lon(params=params)
        self.assert_error_in_response(place_data)
        assert (
            place_data["error"] == constants.UNABLE_TO_GEOCODE_ERROR_MESSAGE
        ), f"Unexpected error, expected {constants.UNABLE_TO_GEOCODE_ERROR_MESSAGE}, got {place_data['error']}"

    def test_addition_lan_and_lon(self):
        """
        Тест на то, как дополняется широта и долгота. Специально была выбрана точка, привязанная к определенному месту,
        но достаточно далекая от него
        """
        near_point_with_existent_address = {"lat": "10.883", "lon": "72.817"}
        params = self.builder.reverse(
            lat=constants.FAR_POINT_LAT, lon=constants.FAR_POINT_LON
        ).params_for_api
        place_data = self.reverse_lat_and_lon(params=params)
        lat = place_data["lat"]
        lon = place_data["lon"]
        self.assert_lat_and_lon(
            valid_lat=near_point_with_existent_address["lat"],
            valid_lon=near_point_with_existent_address["lon"],
            lat=lat,
            lon=lon,
        )
