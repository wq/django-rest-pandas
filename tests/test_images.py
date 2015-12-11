from rest_framework.test import APITestCase
from tests.testapp.models import TimeSeries
import unittest

try:
    import matplotlib
except ImportError:
    matplotlib = None


class ImageTestCase(APITestCase):
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

    @unittest.skipUnless(matplotlib, "requires matplotlib")
    def test_png(self):
        response = self.client.get("/timeseries.png")
        header = response.content[1:4]
        self.assertEqual(header, b"PNG")

    @unittest.skipUnless(matplotlib, "requires matplotlib")
    def test_svg(self):
        response = self.client.get("/timeseries.svg")
        header = response.content[2:5]
        self.assertEqual(header, b"xml")
