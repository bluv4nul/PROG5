"""Импорт модулей по URL: подключает http-адреса к механизму импорта.

Подробное описание работы — в README, раздел «Описание работы кода».
"""

import re
import sys
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

import requests


class URLLoader:
    """Загрузчик: скачивает исходник модуля по URL и выполняет его."""

    def create_module(self, target):
        """None — модуль создаётся стандартным способом."""
        return None

    def exec_module(self, module):
        """Качает код по origin и выполняет его в пространстве имён модуля.

        Если сервер недоступен или файла нет — ImportError.
        """

        try:
            response = requests.get(module.__spec__.origin, timeout=(2, 5))
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise ImportError(
                f"Cannot download remote module: {module.__spec__.origin} "
            ) from error

        source = response.content
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)


class URLFinder(PathEntryFinder):
    """Искатель: знает, какие модули (файлы .py) лежат по одному URL-адресу."""

    def __init__(self, url, available):
        """Запоминает базовый URL и набор доступных имён модулей."""
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        """Спецификация модуля с URLLoader, если имя есть по этому URL, иначе None."""
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)

        else:
            return None


def url_hook(some_str):
    """Для http-элемента sys.path строит URLFinder, иначе ImportError.

    Скачивает листинг каталога и регуляркой собирает из него имена .py-файлов.
    """
    if not some_str.startswith("http"):
        raise ImportError
    try:
        response = requests.get(some_str, timeout=(2, 5))
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Cannot find remote module: {some_str}") from error

    data = response.text
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


class URLPackageFinder(URLFinder):
    """Искатель, который кроме модулей находит пакеты (Сделано Claude)."""

    def is_remote_package(self, short_name):
        """True, если на сервере есть short_name/__init__.py, то есть это пакет."""
        init_url = "{}/{}/__init__.py".format(self.url, short_name)
        try:
            # HEAD — запрос только статуса, без скачивания самого файла.
            response = requests.head(init_url, timeout=(2, 5), allow_redirects=True)
        except requests.exceptions.RequestException:
            return False
        return response.status_code == 200

    def find_spec(self, name, target=None):
        """Спецификация для пакета или модуля, иначе None."""
        # Для "mypackage.subpackage" в папке лежит только "subpackage".
        short_name = name.rpartition(".")[2]

        # Сначала пакет: как и в обычном Python, пакет важнее модуля с тем же именем.
        if self.is_remote_package(short_name):
            package_url = "{}/{}".format(self.url, short_name)
            spec = spec_from_loader(
                name,
                URLLoader(),
                origin=package_url + "/__init__.py",  # код пакета — его __init__.py
                is_package=True,
            )
            # Станет __path__ пакета: здесь Python будет искать его подмодули.
            spec.submodule_search_locations = [package_url]
            return spec

        # Обычный модуль — как в URLFinder, но по короткому имени.
        if short_name in self.available:
            origin = "{}/{}.py".format(self.url, short_name)
            return spec_from_loader(name, URLLoader(), origin=origin)

        return None


def url_package_hook(some_str):
    """Хук с поддержкой пакетов (Сделано Claude).

    Старую работу делает url_hook, результат оборачиваем в URLPackageFinder.
    """
    finder = url_hook(some_str)
    return URLPackageFinder(finder.url, finder.available)


sys.path_hooks.append(url_package_hook)
