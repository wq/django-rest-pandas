import unittest
from rest_framework.test import APITestCase
from tests.testapp.models import TimeSeries
from tests.weather.models import Station
from django.core.management import call_command
import pathlib


DOCS = pathlib.Path("docs")

STATIONS = {
    "MSP": "USW00014922",
    "ATL": "USW00013874",
    "LAX": "USW00023174",
}

class DocsTestCase(APITestCase):
    def setUp(self):
        data = (
            ("2014-01-01", 0.5),
            ("2014-01-02", 0.4),
            ("2014-01-03", 0.6),
            ("2014-01-04", 0.2),
            ("2014-01-05", 0.1),
        )
        for date, value in data:
            TimeSeries.objects.create(date=date, value=value)

        for name, code in STATIONS.items():
            station = Station.objects.create(name=name, code=code)
            station.load_weather()

    def test_docs(self):
        call_command('collectstatic', interactive=False)
        for url in (
            "timeseries.html",
            "timeseries.csv",
            "timeseries.json",
            "timeseries.xlsx",
            "timeseries.png",
            "timeseries.svg",
            "weather.html",
            "weather.csv",
            "weather.json",
            "weather.xlsx",
            "weather.png",
            "weather.svg",
        ):
            response = self.client.get(f"/{url}")
            path = DOCS / url
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.content)
