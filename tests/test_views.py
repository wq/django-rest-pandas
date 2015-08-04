from rest_framework.test import APITestCase
from tests.testapp.models import TimeSeries
from wq.io import load_string
import json
import datetime


class PandasTestCase(APITestCase):
    def setUp(self):
        data = (
            ('2014-01-01', 0.5),
            ('2014-01-02', 0.4),
            ('2014-01-03', 0.6),
            ('2014-01-04', 0.2),
            ('2014-01-05', 0.1),
        )
        for date, value in data:
            TimeSeries.objects.create(date=date, value=value)

    def test_view(self):
        response = self.client.get("/timeseries.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_view_json(self):
        response = self.client.get("/timeseries.json")
        self.assertEqual(response.accepted_media_type, "application/json")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["value"], 0.5)
        self.assertEqual(data[0]["date"], "2014-01-01T00:00:00.000Z")

    def test_view_json_kwargs(self):
        response = self.client.get("/timeseries.json?date_format=epoch")
        self.assertEqual(response.accepted_media_type, "application/json")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["value"], 0.5)
        date = datetime.datetime.utcfromtimestamp(data[0]["date"] / 1000)
        self.assertEqual(date, datetime.datetime(2014, 1, 1))

    def test_viewset(self):
        response = self.client.get("/router/timeseries/.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_no_model(self):
        response = self.client.get("/nomodel.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0].x, '5')

    def load_string(self, response):
        return load_string(response.content.decode('utf-8'))
