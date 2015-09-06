from django.db import models


class TimeSeries(models.Model):
    date = models.DateField()
    value = models.FloatField()


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
