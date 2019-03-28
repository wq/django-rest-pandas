import unittest
from rest_framework.test import APITestCase
from tests.testapp.models import TimeSeries, CustomIndexSeries
from wq.io import load_string
import json
import datetime
import os
from .settings import HAS_DJANGO_PANDAS


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
            CustomIndexSeries.objects.create(
                code='v' + date.replace('-', ''),
                value=value,
            )

    def test_view_csv(self):
        response = self.client.get("/timeseries.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_view_csv_noid(self):
        response = self.client.get("/timeseriesnoid.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    @unittest.skipUnless(HAS_DJANGO_PANDAS, 'requires django-pandas')
    def test_view_django_pandas(self):
        response = self.client.get("/djangopandas.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_view_json(self):
        response = self.client.get("/timeseries.json")
        self.assertEqual(response.accepted_media_type, "application/json")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 5)
        self.assertIn('id', data[0])
        self.assertEqual(data[0]["id"], 1)
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

        response = self.client.get("/timeseries.json?orient=index")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data.values()), 5)
        self.assertEqual(data["1"]["value"], 0.5)

    def test_view_html(self):
        response = self.client.get("/timeseries?test=1")
        expected = open(
            os.path.join(os.path.dirname(__file__), 'files', 'timeseries.html')
        ).read()
        self.assertHTMLEqual(expected, response.content.decode('utf-8'))

    def test_viewset(self):
        response = self.client.get("/router/timeseries.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_mixed_renderer_csv(self):
        response = self.client.get("/mixedrenderers.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_mixed_renderer_api(self):
        response = self.client.get("/mixedrenderers.api")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_mixed_renderer_json(self):
        response = self.client.get("/mixedrenderers.json")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['value'], 0.5)

    def test_custom_csv_date_format(self):
        response = self.client.get("/customcsv.csv")
        data = self.load_string(response)
        self.assertEqual(data[0].date, '01-01-2014')

    def test_pandas_mixin(self):
        response = self.client.get("/mixin.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].value, '0.5')

    def test_pandas_no_mixin(self):
        with self.assertRaises(Exception) as e:
            self.client.get("/nomixin.csv")
        self.assertEqual(
            e.exception.args[0],
            "Response data is a ReturnList, not a DataFrame! "
            "Did you extend PandasMixin?"
        )

    def test_no_model(self):
        response = self.client.get("/nomodel.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0].x, '5')

    def test_from_file(self):
        response = self.client.get("/fromfile.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0].x, '5')

    def test_customindex_csv(self):
        response = self.client.get("/customindex.csv")
        data = self.load_string(response)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].code, 'v20140101')
        self.assertEqual(data[0].value, '0.5')

    def test_customindex_json(self):
        response = self.client.get("/customindex.json")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['code'], 'v20140101')
        self.assertEqual(data[0]['value'], 0.5)

        response = self.client.get("/customindex.json?orient=index")
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 5)
        self.assertEqual(data['v20140101']['value'], 0.5)

    def load_string(self, response):
        return load_string(response.content.decode('utf-8'))
