import pytest

import apis
import constants
from base_case import ApiBase


@pytest.mark.API
class TestSimpleSearch(ApiBase):
    """
    Тесты для простого поиска по адресу/названию (Вкладка Search -> Simple)
    """

    parametrize_addresses = [
        {
            "name": "Санкт-Петербург, Проспект Большевиков 22к1",
            "lat": "59",
            "lon": "30.4"
        },
        {"name": "Санкт-Петербург, Загребский бульвар 9", "lat": "59.8", "lon": "30"},
        {"name": "Tokio Cat Street 6", "lat": "35", "lon": "139"},
        {"name": "New York Amanda Way 5", "lat": "40.8", "lon": "-72.7"}
    ]

    parametrize_names = [
        {"name": "Московский Кремль", "lat": "55.75", "lon": "37.61"},
        {"name": "France Eiffel Tower", "lat": "48.85", "lon": "2.29"},
        {"name": "England Big Ben", "lat": "51.5", "lon": "-0.12"},
        {"name": "Пирамида Хеопса", "lat": "29.97", "lon": "31.13"}
    ]

    language_combination_address_data = {
        "address": "Saint-Petersburg, Загребский бульвар 9",
        "lat": "59.8",
        "lon": "30"
    }

    @pytest.mark.parametrize("valid_name_data", parametrize_names)
    def test_search_name_parametrized(self, valid_name_data):
        """
        Параметризированный тест на на поиск точки на карте по названию места.
        Подобные тесты могут быстро перестать быть актуальными (в связи с закрытием заведения, например), поэтому
        в качестве тестовых данных были выбраны известные места, местоположение которых вряд ли изменится.
        Для исключения ошибок, для сравнения ответа отбирается только точка, название которой максимально соответствует
        введённому (первая в списке выдачи точка).
        Также неизвестно, что выдают запросы в качестве place_id, может ли этот id менятся, поэтому проверяются
        именно широта и долгота - lat и lon. В принципе, проверка адреса в ответе на запрос тоже имеет место быть. Но
        адрес, в отличие от широты и долготы, поменятся может.

        Проверяет правильность выдачи широты и долготы заранее определенных названий мест.
        Проверяет в том числе места, написанные на английском языке, места в других странах.
        """
        params = self.builder.search(address=valid_name_data["name"]).params_for_api
        response_name_data = self.search_address_or_name(params=params)
        name_data_from_response = response_name_data[0]
        lat = name_data_from_response["lat"]
        lon = name_data_from_response["lon"]
        self.assert_lat_and_lon(
            valid_lat=valid_name_data["lat"],
            valid_lon=valid_name_data["lon"],
            lat=lat,
            lon=lon
        )

    @pytest.mark.parametrize("valid_address_data", parametrize_addresses)
    def test_search_address_parametrized(self, valid_address_data):
        """
        Параметризированный тест на на поиск точки на карте по адресу.
        Как тесты на поиск места по названия, только на адреса. Отличается проверка. Так как по адресу выдает список из
        всех магазинов, заведений, которые находятся по адресу - ширина и долгота имеют больший разброс (вдруг
        какое-то заведение закроется, это очень возможно, тогда первым в списке будет уже другое заведение), соответственно
        ширина и долгота изменится. Поэтому в тестовых данных lat и lon для данной проверки могут задаваться с некоторым заделом"""
        params = self.builder.search(address=valid_address_data["name"]).params_for_api
        response_address_data = self.search_address_or_name(params=params)
        address_data_from_response = response_address_data[0]
        lat = address_data_from_response["lat"]
        lon = address_data_from_response["lon"]
        self.assert_lat_and_lon(
            valid_lat=valid_address_data["lat"],
            valid_lon=valid_address_data["lon"],
            lat=lat,
            lon=lon
        )

    def test_non_existent_address_search(self):
        """
        Тест на запрос с несуществующим адресом
        """
        params = self.builder.search(
            address=constants.NON_EXISTENT_ADDRESS
        ).params_for_api
        response_data = self.search_address_or_name(params=params)
        self.assert_response_is_empty_list(response=response_data)

    def test_empty_address_search(self):
        """
        Тест на запрос пустым адресом
        """
        params = self.builder.search(address="").params_for_api
        response_data = self.search_address_or_name(params=params)
        print(response_data)
        self.assert_response_is_empty_list(response=response_data)

    def test_space_address_search(self):
        """
        Тест на запрос с адресом, заданным пробелом
        """
        params = self.builder.search(address=" ").params_for_api
        response_data = self.search_address_or_name(params=params)
        self.assert_response_is_empty_list(response=response_data)

    def test_limit_search(self):
        """
        Тест на проверку работы опции 'maximum number of results' (параметра 'limit' в запросе)
        """
        params = self.builder.search(
            address=constants.ADDRESS_WITH_MANY_RESULTS,
            limit=constants.LIMIT_FOR_LIMIT_TEST
        ).params_for_api
        response_data = self.search_address_or_name(params=params)
        assert (
            len(response_data) == constants.LIMIT_FOR_LIMIT_TEST
        ), f"Wrong count of results, expected {constants.LIMIT_FOR_LIMIT_TEST}"

    def test_countrycode_search(self):
        """
        Тест на проверку работы опции 'Contry Codes' (параметра 'countrycodes' в запросе) - для выдачи
        результатов только в определенных странах
        """
        params = self.builder.search(
            address=constants.ADDRESS_WITH_MANY_RESULTS,
            countrycodes=constants.DEUTSCHLAND_COUNTRY_CODE
        ).params_for_api
        response_data = self.search_address_or_name(params=params)
        display_name = response_data[0]["display_name"]
        assert (
            "Deutschland" in display_name
        ), f"Wrong response, expected result only with 'Deutschland' word, got {display_name}"

    def test_language_combination_search(self):
        """
        Тест на запрос с адресом, в котором используются одновременно несколько языков
        """
        valid_address_data = self.language_combination_address_data
        params = self.builder.search(
            address=valid_address_data["address"]
        ).params_for_api
        response_data = self.search_address_or_name(params=params)
        address_data_from_response = response_data[0]
        lat = address_data_from_response["lat"]
        lon = address_data_from_response["lon"]
        assert (
            valid_address_data["lat"] in lat and valid_address_data["lon"] in lon
        ), f"Wrong latitude/longitude, expected {valid_address_data['lat'], valid_address_data['lon']}, got {lat, lon}"

    def test_too_big_address(self):
        """
        Тест на запрос со слишком большим адресом - должен возвращать 414 ошибку (Request URI Too Large)
        Код ошибки проверяется внутри метода для запроса
        """
        params = self.builder.search(address=constants.TO_BIG_ADDRESS).params_for_api
        self.api_client.request_custom(
            method="GET",
            location=apis.SEARCH_API_LOCATION,
            params=params,
            expected_status=414,
            jsonify=False
        )


@pytest.mark.API
class TestStructuredSearch(ApiBase):
    """
    Тесты для структурированного поиска по адресу (Вкладка Search -> Sctructured)
    """

    data_for_valid_structure_request = {
        "city": "Санкт-Петербург",
        "country": "Россия",
        "street": "Загребский бульвар"
    }

    def test_structure_search(self):
        """
        Позитивный тест на структурированный поиск
        """
        request_data = self.data_for_valid_structure_request
        params = self.builder.search(
            structured=True,
            city=request_data["city"],
            country=request_data["country"],
            street=request_data["street"]
        ).params_for_api
        response = self.search_address_or_name(params=params)
        self.assert_display_name_from_response(
            response=response[0],
            expected_words=[
                request_data["city"],
                request_data["country"],
                request_data["street"]
            ]
        )

    def test_structure_search_without_data(self):
        """
        Тест на структурированный поиск без заполнения полей (city=None, country=None, etc)
        """
        params = self.builder.search(structured=True).params_for_api
        response = self.search_address_or_name(params=params)
        self.assert_response_is_empty_list(response=response)

    def test_structure_search_with_word_in_postal_code_field(self):
        """
        Тест на структурированный поиск с полем "Postal Code" в виде слова
        """
        word_postal_code = "aaa"
        params = self.builder.search(
            structured=True,
            city=self.data_for_valid_structure_request["city"],
            postalcode=word_postal_code
        ).params_for_api
        response = self.search_address_or_name(params=params)
        self.assert_response_is_empty_list(response=response)
