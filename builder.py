from dataclasses import dataclass


class Builder:
    """
    Датаклассы для составления params/data к запросам
    """

    @staticmethod
    def search(
        address=None,
        structured=False,
        params_for_api=None,
        limit=None,
        countrycodes=None,
        city=None,
        country=None,
        street=None,
        postalcode=None
    ):
        """
        Датакласс для создания params к api на точки на карте по адресу (search)
        По умолчанию билдит параметры для запросов с 'simple' адресом - адресом в видео одной обычной строки
        Но при использовании параметра structured=True билдит параметры уже для запросов со структурированным адресом -
        где город, страна, улица и т.д. находятся в отдельных полях
        """

        @dataclass
        class Search:
            """
            Датакласс для сегментов
            """

            params_for_api: dict

        if params_for_api is None and not structured:
            params_for_api = {
                "q": address,
                "format": "jsonv2",
                "limit": limit,
                "countrycodes": countrycodes
            }

        if params_for_api is None and structured:
            params_for_api = {
                "street": street,
                "city": city,
                "country": country,
                "postalcode": postalcode,
                "format": "jsonv2"
            }
        return Search(params_for_api=params_for_api)

    @staticmethod
    def reverse(lat=None, lon=None, params_for_api=None):
        @dataclass
        class Reverse:
            """
            Датакласс для создания params к api на получение адреса по точке на карте (reverse)
            """

            params_for_api: dict

        if params_for_api is None:
            params_for_api = {"lat": lat, "lon": lon, "format": "jsonv2"}
        return Reverse(params_for_api=params_for_api)
