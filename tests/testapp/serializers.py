from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_pandas import PandasUnstackedSerializer
from .models import (
    TimeSeries, MultiTimeSeries, ComplexTimeSeries, CustomIndexSeries,
)


class TimeSeriesSerializer(ModelSerializer):
    date = serializers.DateField(format=None)

    class Meta:
        model = TimeSeries
        fields = '__all__'


class TimeSeriesNoIdSerializer(TimeSeriesSerializer):
    class Meta:
        model = TimeSeries
        exclude = ['id']


class MultiTimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        exclude = ['id']

        pandas_index = ['date']
        pandas_unstacked_header = ['series']
        pandas_scatter_coord = ['series']
        pandas_boxplot_group = 'series'
        pandas_boxplot_date = 'date'


class ComplexTimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = ComplexTimeSeries
        exclude = ['id']

        pandas_index = ['date', 'type']
        pandas_unstacked_header = ['site', 'parameter', 'units']


class ComplexScatterSerializer(ComplexTimeSeriesSerializer):
    class Meta(ComplexTimeSeriesSerializer.Meta):
        exclude = ['id', 'flag']

        pandas_scatter_coord = ['units', 'parameter']
        pandas_scatter_header = ['site']


class ComplexBoxplotSerializer(ComplexTimeSeriesSerializer):
    class Meta(ComplexTimeSeriesSerializer.Meta):
        exclude = ['id', 'flag', 'type']
        pandas_boxplot_group = 'site'
        pandas_boxplot_date = 'date'
        pandas_boxplot_header = ['units', 'parameter']


class NotUnstackableSerializer(ModelSerializer):
    class Meta:
        model = MultiTimeSeries
        fields = '__all__'
        list_serializer_class = PandasUnstackedSerializer
        # pandas_unstacked_header = Missing
        pandas_index = ['series']


class CustomIndexSeriesSerializer(ModelSerializer):
    class Meta:
        model = CustomIndexSeries
        fields = '__all__'
