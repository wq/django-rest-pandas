from rest_framework.test import APITestCase
from tests.testapp.models import MultiTimeSeries
from tests.testapp.serializers import NotUnstackableSerializer
from rest_pandas.test import parse_csv
from django.core.exceptions import ImproperlyConfigured


class MultiTestCase(APITestCase):
    def setUp(self):
        data = (
            ('test1', '2015-01-01', 0.5),
            ('test1', '2015-01-02', 0.4),
            ('test1', '2015-01-03', 0.6),
            ('test1', '2015-01-04', 0.2),
            ('test1', '2015-01-05', 0.1),

            ('test2', '2015-01-01', 0.7),
            ('test2', '2015-01-02', 0.8),
            ('test2', '2015-01-03', 0.0),
            ('test2', '2015-01-04', 0.9),
            ('test2', '2015-01-05', 0.3),
        )
        for series, date, value in data:
            MultiTimeSeries.objects.create(
                series=series,
                date=date,
                value=value
            )

    def test_multi_series(self):
        response = self.client.get("/multitimeseries.csv")
        self.assertEqual(
            """,value,value
            series,test1,test2
            date,,
            2015-01-01,0.5,0.7
            2015-01-02,0.4,0.8
            2015-01-03,0.6,0.0
            2015-01-04,0.2,0.9
            2015-01-05,0.1,0.3
            """.replace(' ', ''),
            response.content.decode('utf-8'),
        )
        datasets = self.parse_csv(response)
        self.assertEqual(len(datasets), 2)
        for dataset in datasets:
            self.assertEqual(len(dataset['data']), 5)

        if datasets[0]['series'] == "test1":
            s1data, s2data = datasets[0], datasets[1]
        else:
            s2data, s1data = datasets[1], datasets[0]

        d0 = s1data['data'][0]
        self.assertEqual(d0['date'], '2015-01-01')
        self.assertEqual(d0['value'], 0.5)

        d0 = s2data['data'][4]
        self.assertEqual(d0['date'], '2015-01-05')
        self.assertEqual(d0['value'], 0.3)

    def test_multi_scatter(self):
        response = self.client.get("/multiscatter.csv")
        self.assertEqual(
            """date,test1-value,test2-value
            2015-01-01,0.5,0.7
            2015-01-02,0.4,0.8
            2015-01-03,0.6,0.0
            2015-01-04,0.2,0.9
            2015-01-05,0.1,0.3
            """.replace(' ', ''),
            response.content.decode('utf-8')
        )

    def test_not_unstackable(self):
        qs = MultiTimeSeries.objects.all()
        with self.assertRaises(ImproperlyConfigured) as e:
            NotUnstackableSerializer(qs, many=True).data
        self.assertEqual(
            e.exception.args[0],
            "pandas_unstacked_header should be specified on "
            "NotUnstackableSerializer.Meta"
        )

    def parse_csv(self, response):
        return parse_csv(response.content.decode('utf-8'))
