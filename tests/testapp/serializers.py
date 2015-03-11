from rest_framework.serializers import ModelSerializer
from .models import TimeSeries


class TimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = TimeSeries
