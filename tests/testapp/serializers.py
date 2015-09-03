from rest_framework.serializers import ModelSerializer
from rest_pandas import PandasUnstackedSerializer
from .models import TimeSeries, MultiTimeSeries, ComplexTimeSeries


class TimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = TimeSeries


class MultiTimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        pandas_header_fields = ['series']
        pandas_index_fields = ['date']
        exclude = ['id']


class MultiScatterSerializer(ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        pandas_scatter_fields = ['series']
        pandas_header_fields = []
        pandas_index_fields = ['date']
        exclude = ['id']


class ComplexTimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = ComplexTimeSeries
        pandas_header_fields = ['site', 'parameter', 'units']
        pandas_index_fields = ['date', 'type']
        exclude = ['id']


class ComplexScatterSerializer(ModelSerializer):
    class Meta:
        model = ComplexTimeSeries
        pandas_scatter_fields = ['units', 'parameter']
        pandas_header_fields = ['site']
        pandas_index_fields = ['date', 'type']
        exclude = ['id', 'flag']


class NotUnstackableSerializer(ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        list_serializer_class = PandasUnstackedSerializer
        # pandas_header_fields = Missing
        pandas_index_fields = ['series']
