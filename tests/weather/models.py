from django.db import models
import requests


DATA_URL = "https://www.ncei.noaa.gov/access/past-weather/{code}/data.csv"


class Station(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def load_weather(self):
        response = requests.get(DATA_URL.format(code=self.code))

        for i, row in enumerate(response.iter_lines(decode_unicode=True)):
            if i < 2:
                continue
            assert row.count(",") == 6
            date, tavg, tmax, tmin, prcp, snow, snwd = row.split(",")
            if date < '2020-01-01':
                continue
            self.weather_set.create(
                date=date,
                tavg=tavg or None,
                tmax=tmax or tavg,
                tmin=tmin,
                prcp=prcp or None,
                snow=snow or None,
                snwd=snwd or None,
            )


class Weather(models.Model):
    station = models.ForeignKey(Station, on_delete=models.PROTECT)
    date = models.DateField(verbose_name="Date")
    tavg = models.IntegerField(verbose_name="Average Temp (°F)", null=True)
    tmax = models.IntegerField(verbose_name="Max Temp (°F)")
    tmin = models.IntegerField(verbose_name="Min Temp (°F)")
    prcp = models.FloatField(verbose_name="Precipitation (in)")
    snow = models.FloatField(verbose_name="Snow (in)", null=True)
    snwd = models.FloatField(verbose_name="Snow Depth (in)", null=True)
