"""Импорт модулей по URL: подключает http-адреса к механизму импорта."""

import re
import sys
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

import requests


class URLLoader:
    """Скачивает исходник модуля по URL и выполняет его."""

    def create_module(self, target):
        """None — модуль создаётся стандартным способом."""
        return None

    def exec_module(self, module):
        """Качает код по origin и выполняет его в пространстве имён модуля."""

        response = requests.get(module.__spec__.origin, timeout=(2, 10))
        response.raise_for_status()
        source = response.content
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)


class URLFinder(PathEntryFinder):
    """Знает, какие модули лежат по одному URL-адресу."""

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
    """Для http-элемента sys.path строит URLFinder, иначе ImportError."""
    if not some_str.startswith("http"):
        raise ImportError
    response = requests.get(some_str, timeout=(2, 10))
    response.raise_for_status()
    data = response.text
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)
