import unittest
from rest_framework.test import APITestCase
from tests.testapp.models import MultiTimeSeries
from tests.testapp.serializers import NotUnstackableSerializer
from rest_pandas.test import parse_csv
from django.core.exceptions import ImproperlyConfigured
import os
from .settings import HAS_MATPLOTLIB
import pandas


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

    def test_multi_series_html(self):
        response = self.client.get("/multitimeseries.html")
        expected = open(os.path.join(
            os.path.dirname(__file__), 'files', 'multitimeseries.html'
        )).read()
        self.assertHTMLEqual(expected, response.content.decode('utf-8'))

    def test_multi_scatter(self):
        response = self.client.get("/multiscatter.csv")
        if pandas.__version__ == "0.20.3":
            # FIXME: Remove when dropping Python 3.4 support
            header = "date,test1-value,test2-value"
        else:
            header = ",test1-value,test2-value\ndate,,"
        self.assertEqual(header + """
            2015-01-01,0.5,0.7
            2015-01-02,0.4,0.8
            2015-01-03,0.6,0.0
            2015-01-04,0.2,0.9
            2015-01-05,0.1,0.3
            """.replace(' ', ''),
            response.content.decode('utf-8')
        )

    @unittest.skipUnless(HAS_MATPLOTLIB, "requires matplotlib")
    def test_multi_boxplot(self):
        # Default: group=series-year
        response = self.client.get("/multiboxplot.csv")

        datasets = self.parse_csv(response)
        self.assertEqual(len(datasets), 2)
        if datasets[0]['series'] == 'test1':
            s1data, s2data = datasets
        else:
            s2data, s1data = datasets

        self.assertEqual(len(s1data['data']), 1)
        stats = s1data['data'][0]
        self.assertEqual(stats['year'], '2015')
        self.assertEqual(stats['value-whislo'], 0.1)
        self.assertEqual(stats['value-mean'], 0.36)
        self.assertEqual(stats['value-whishi'], 0.6)

        stats = s2data['data'][0]
        self.assertEqual(stats['year'], '2015')
        self.assertEqual(stats['value-whislo'], 0.0)
        self.assertEqual(round(stats['value-mean'], 8), 0.54)
        self.assertEqual(stats['value-whishi'], 0.9)

    @unittest.skipUnless(HAS_MATPLOTLIB, "requires matplotlib")
    def test_multi_boxplot_series(self):
        response = self.client.get("/multiboxplot.csv?group=series")
        datasets = self.parse_csv(response)[0]['data']
        self.assertEqual(len(datasets), 2)
        if datasets[0]['series'] == 'test1':
            s1data, s2data = datasets
        else:
            s2data, s1data = datasets

        stats = s1data
        self.assertNotIn('year', stats)
        self.assertEqual(stats['value-whislo'], 0.1)
        self.assertEqual(stats['value-mean'], 0.36)
        self.assertEqual(stats['value-whishi'], 0.6)

        stats = s2data
        self.assertNotIn('year', stats)
        self.assertEqual(stats['value-whislo'], 0.0)
        self.assertEqual(round(stats['value-mean'], 8), 0.54)
        self.assertEqual(stats['value-whishi'], 0.9)

    @unittest.skipUnless(HAS_MATPLOTLIB, "requires matplotlib")
    def test_multi_boxplot_series_month(self):
        response = self.client.get("/multiboxplot.csv?group=series-month")

        datasets = self.parse_csv(response)
        self.assertEqual(len(datasets), 2)
        if datasets[0]['series'] == 'test1':
            s1data, s2data = datasets
        else:
            s2data, s1data = datasets

        self.assertEqual(len(s1data['data']), 1)
        stats = s1data['data'][0]
        self.assertEqual(stats['month'], '1')
        self.assertEqual(stats['value-whislo'], 0.1)
        self.assertEqual(stats['value-mean'], 0.36)
        self.assertEqual(stats['value-whishi'], 0.6)

        stats = s2data['data'][0]
        self.assertEqual(stats['month'], '1')
        self.assertEqual(stats['value-whislo'], 0.0)
        self.assertEqual(round(stats['value-mean'], 8), 0.54)
        self.assertEqual(stats['value-whishi'], 0.9)

    @unittest.skipUnless(HAS_MATPLOTLIB, "requires matplotlib")
    def test_multi_boxplot_year(self):
        response = self.client.get("/multiboxplot.csv?group=year")

        datasets = self.parse_csv(response)[0]['data']
        self.assertEqual(len(datasets), 1)
        stats = datasets[0]
        self.assertEqual(stats['year'], 2015)
        self.assertEqual(stats['value-whislo'], 0.0)
        self.assertEqual(stats['value-mean'], 0.45)
        self.assertEqual(stats['value-whishi'], 0.9)

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
