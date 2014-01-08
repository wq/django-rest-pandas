from django.db import models


class TimeSeries(models.Model):
    date = models.DateField()
    value = models.FloatField()
