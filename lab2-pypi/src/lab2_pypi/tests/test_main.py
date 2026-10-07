import pytest

from lab2_pypi.main import GetCurrencies, ConvertToCSV, ConvertToYAML, FILES_DIR

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

MOCK_SUCCESS_RESPONSE = {
    "Date": "2024-01-01T11:30:00+03:00",
    "Valute": {
        "USD": {
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 90.12,
            "Previous": 89.80
        },
        "EUR": {
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 97.45,
            "Previous": 97.10
        }
    }
}

MOCK_INVALID_RESPOSE = {
    "Date": "2024-01-01T11:30:00+03:00"
}



def test_getcurrencies_succes(requests_mock):
    """
    Проверка успешного ответа
    """

    requests_mock.get(CBR_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = GetCurrencies()
    data = obj.getCurrencies()

    assert isinstance(data, dict)
    assert "USD" in data
    assert "CharCode" in data["USD"]
    assert "Value" in data["USD"]

def test_getcurrencies_invalid(requests_mock):
    """
    Проверка не успешного ответа
    """

    requests_mock.get(CBR_URL, json=MOCK_INVALID_RESPOSE, status_code=200)

    obj = GetCurrencies()
    with pytest.raises(KeyError):
        data = obj.getCurrencies()

EXPECTED_CSV_ROWS = [
    {
        "ID_Валюты": "USD",
        "NumCode": "840",
        "CharCode": "USD",
        "Nominal": 1,
        "Name": "Доллар США",
        "Value": 90.12,
        "Previous": 89.80
    },
    {
        "ID_Валюты": "EUR",
        "NumCode": "978",
        "CharCode": "EUR",
        "Nominal": 1,
        "Name": "Евро",
        "Value": 97.45,
        "Previous": 97.10
    }
]

def test_csv_getcurrencies(requests_mock):
    requests_mock.get(CBR_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = ConvertToCSV(GetCurrencies())
    data = obj.getCurrencies()

    assert data == EXPECTED_CSV_ROWS
    assert isinstance(data, list)
    assert len(data) > 0

def test_csv_createfile(requests_mock):
    requests_mock.get(CBR_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = ConvertToCSV(GetCurrencies())
    data = obj.getCurrencies()
    obj.createFile()

    with open(FILES_DIR / "result_in_csv.csv", mode="r", encoding="utf-8") as file:
        text = file.read()
        assert "ID_Валюты" in text
        assert ";" in text

def test_yaml_getcurrencies(requests_mock):
    requests_mock.get(CBR_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = ConvertToYAML(GetCurrencies())
    data = obj.getCurrencies()

    assert isinstance(data, dict)
    assert "USD" in data
    assert "CharCode" in data["USD"]
    assert "Value" in data["USD"]
    

def test_yaml_createfile(requests_mock):
    requests_mock.get(CBR_URL, json=MOCK_SUCCESS_RESPONSE, status_code=200)

    obj = ConvertToYAML(GetCurrencies())
    data = obj.getCurrencies()
    obj.createFile()

    with open(FILES_DIR / "result_in_yaml.yaml", mode="r", encoding="utf-8") as file:
        text = file.read()
        assert "USD" in text
        assert "Value" in text
