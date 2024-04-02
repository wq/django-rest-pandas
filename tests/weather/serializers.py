from rest_framework import serializers
from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    station = serializers.ReadOnlyField(source="station.name", label="Station")

    class Meta:
        model = Weather
        exclude = ["id"]
        pandas_index = ["date"]  # Date
        pandas_unstacked_header = ["Station"]
