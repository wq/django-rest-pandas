from rest_framework.serializers import ModelSerializer, DateField
from rest_pandas import PandasUnstackedSerializer
from .models import TimeSeries, MultiTimeSeries, ComplexTimeSeries
from rest_pandas import USE_LIST_SERIALIZERS


if not USE_LIST_SERIALIZERS:
    # DRF 2.4 appended 00:00:00 to dates
    class DateField(DateField):
        def to_native(self, date):
            return str(date)


class TimeSeriesSerializer(ModelSerializer):
    class Meta:
        model = TimeSeries


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
    date = DateField()

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


if USE_LIST_SERIALIZERS:
    class NotUnstackableSerializer(ModelSerializer):
        class Meta:
            model = MultiTimeSeries
            list_serializer_class = PandasUnstackedSerializer
            # pandas_unstacked_header = Missing
            pandas_index = ['series']
else:
    class NotUnstackableSerializer(ModelSerializer, PandasUnstackedSerializer):
        class Meta:
            model = MultiTimeSeries
            # pandas_unstacked_header = Missing
            pandas_index = ['series']
