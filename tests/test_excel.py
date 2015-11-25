from rest_framework.test import APITestCase
from tests.testapp.models import TimeSeries
from wq.io import load_file


class ExcelTestCase(APITestCase):
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

    def test_xls(self):
        response = self.client.get("/timeseries.xls")
        xlfile = open('tests/output.xls', 'wb')
        xlfile.write(response.content)
        xlfile.close()

        data = load_file("tests/output.xls")
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].date.year, 2014)
        self.assertEqual(data[0].value, 0.5)

    def test_xlsx(self):
        response = self.client.get("/timeseries.xlsx")
        xlfile = open('tests/output.xlsx', 'wb')
        xlfile.write(response.content)
        xlfile.close()

        data = load_file("tests/output.xlsx")
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0].date.year, 2014)
        self.assertEqual(data[0].value, 0.5)
