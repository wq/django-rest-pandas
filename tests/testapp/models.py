from django.db import models
from django_pandas.managers import DataFrameManager


class TimeSeries(models.Model):
    date = models.DateField()
    value = models.FloatField()

    objects = DataFrameManager()


class MultiTimeSeries(models.Model):
    # Header
    series = models.CharField(max_length=5)

    # Index
    date = models.DateField()

    # Values
    value = models.FloatField()


class ComplexTimeSeries(models.Model):
    # Header
    site = models.CharField(max_length=5)
    parameter = models.CharField(max_length=5)
    units = models.CharField(max_length=5, null=True, blank=True)

    # Index
    date = models.DateField()
    type = models.CharField(max_length=10)

    # Values
    value = models.FloatField()
    flag = models.CharField(max_length=1, null=True, blank=True)


class CustomIndexSeries(models.Model):
    code = models.SlugField(primary_key=True)
    value = models.FloatField()
