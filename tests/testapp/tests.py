from rest_framework.test import APITestCase
from .models import TimeSeries
from wq.io import load_string
import json


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
        data = load_string(unicode(response.content))
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_view_json(self):
        response = self.client.get("/timeseries.json")
        self.assertEqual(response.accepted_media_type, "application/json")
        data = load_string(unicode(response.content))
        data = json.loads(response.content)
        self.assertEqual(len(data.keys()), 5)
        self.assertEqual(data["1"]["value"], 0.5)

    def test_viewset(self):
        response = self.client.get("/router/timeseries/.csv")
        data = load_string(unicode(response.content))
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_no_model(self):
        response = self.client.get("/nomodel.csv")
        data = load_string(unicode(response.content))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0].x, '5')
