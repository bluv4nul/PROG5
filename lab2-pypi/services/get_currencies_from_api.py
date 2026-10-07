import httpx
import xml.etree.ElementTree as ET
from models.models import Currency


async def get_currencies_from_api(
    url: str = "https://www.cbr.ru/scripts/XML_daily.asp",
) -> list[Currency]:
    """Получает данные о валютах с API"""

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    data = ET.fromstring(response.text)
    currencies: list[Currency] = []

    for valute in data.findall("Valute"):
        code_el = valute.find("CharCode")
        name_el = valute.find("Name")
        value_el = valute.find("Value")

        if code_el is None or name_el is None or value_el is None:
            raise ValueError("Некорректные данные в XML")

        code = code_el.text
        name = name_el.text
        value_text = value_el.text

        if code is None or name is None or value_text is None:
            raise ValueError("Некорректные данные в XML")

        currencies.append(
            Currency(
                code=code,
                name=name,
                value=float(value_text.replace(",", ".")),
            )
        )

    return currencies
