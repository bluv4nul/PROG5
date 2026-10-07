import requests, json, csv, yaml
from typing import Any
from abc import *
from pathlib import Path

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
FILES_DIR = Path(__file__).parent / "files"


class Currencies(ABC):
    """
    Базовое поведение программы.

    Имеет два метода - получение данныных валют getCurrencies() и создание файла createFile()

    Реализован с использованием ABC
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def getCurrencies(self) -> Any:
        pass

    @abstractmethod
    def createFile(self) -> None:
        pass


class GetCurrencies(Currencies):
    """
    class concreteComponent(Component):

    Принимает Currencies как родительский метод

    getCurrencies() - в данном случае возвращает dict, что соотвествует json файлам
    """

    def getCurrencies(self, url=CBR_URL) -> dict:

        response = requests.get(url)
        response.raise_for_status()

        self.data = response.json()

        if "Valute" not in self.data:
            raise KeyError(
                "Данные повреждены или получены неправильно, отсутвует информация о валютах"
            )
        else:
            self.data = self.data["Valute"]
            return self.data

    def createFile(self) -> None:
        if hasattr(self, "data"):
            with open(FILES_DIR / "result_in_json.json", "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False)
        else:
            raise ValueError("Сначала вызовите getCurrencies()")


class Convert(Currencies):
    """
    Декоратор, описывающий общее поведение декораторов

    Так же имеет два метода:

    getCurrencies() - переводит в нужный формат и возвращать значение

    createFile() - создает файл в нужном формате
    """

    _currencies: Currencies = None

    def __init__(self, currencies: Currencies) -> None:
        self._currencies = currencies

    def currencies(self) -> Currencies:
        return self._currencies

    def getCurrencies(self) -> object:
        return self._currencies.getCurrencies()

    def createFile(self) -> None:
        return self._currencies.createFile()


class ConvertToCSV(Convert):
    """
    Декоратор переводящий JSON формат в CSV формат

    Наследует класс Convert

    getCurrencies() - в этом случает вовзвращает list[dict[str, any]], что соотвествует формату csv
        [{"key": value, ...}, ...]
        Метод сохраняет переменные self._column и self._rows для дальнейшей удобной записи в файл

    createFile() - создает файл в формате csv
    """

    def getCurrencies(self) -> list[dict[str, Any]]:

        data = self._currencies.getCurrencies()
        if data:
            first_key = next(iter(data))

            self._columns = ["ID_Валюты"] + list(data[first_key].keys())

            self._rows = []

            for key in data:
                row = {"ID_Валюты": key}
                info = data[key]
                for i in info:
                    row[i] = info[i]
                self._rows.append(row)

            return self._rows
        else:
            raise ValueError("Нет данных о валютах")

    def createFile(self):
        if hasattr(self, "_rows") and hasattr(self, "_columns"):
            with open(
                FILES_DIR / "result_in_csv.csv", "w", encoding="utf-8", newline=""
            ) as file:
                writer = csv.DictWriter(file, fieldnames=self._columns, delimiter=";")
                writer.writeheader()
                writer.writerows(self._rows)
        else:
            raise ValueError("Сначала вызоваите getCurrencies")


class ConvertToYAML(Convert):
    """
    Декоратор переводящий JSON формат в YAML формат

    Наследует класс Convert

    getCurrencies() - в этом случает вовзвращает dict, что соотвествует формату json, по факту являющимся более строгим Yaml`ом
        Метод сохраняет переменную self.data для дальнейшей удобной записи в файл

    createFile() - создает файл в формате Yaml
    """

    def getCurrencies(self) -> dict:

        self.data = self._currencies.getCurrencies()

        return self.data

    def createFile(self) -> None:
        if hasattr(self, "data"):
            with open(FILES_DIR / "result_in_yaml.yaml", "w", encoding="utf-8") as file:
                yaml.dump(data=self.data, stream=file, allow_unicode=True)
        else:
            raise ValueError("Сначала вызовите getCurrencies")
