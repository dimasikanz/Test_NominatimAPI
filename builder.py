from dataclasses import dataclass


class Builder:
    """
    Датаклассы для составления params/data к запросам
    """

    @staticmethod
    def search(address, params_for_api=None):
        """
        Датакласс для создания params к api на точки на карте по адресу (search)
        """
        @dataclass
        class Search:
            """
            Датакласс для сегментов
            """
            params_for_api: dict
        if params_for_api is None:
            params_for_api = { }
        return Search(params_for_api=params_for_api)

    @staticmethod
    def reverse(
        lat,
        lon,
        params_for_api=None,
    ):
        @dataclass
        class Reverse:
            """
            Датакласс для создания params к api на получение адреса по точке на карте (reverse)
            """
            params_for_api: dict
        if params_for_api is None:
            params_for_api = { }
        return Reverse(params_for_api=params_for_api)