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
    date = DateField()

    class Meta:
        model = ComplexTimeSeries
        pandas_header_fields = ['site', 'parameter', 'units']
        pandas_index_fields = ['date', 'type']
        exclude = ['id']


class ComplexScatterSerializer(ModelSerializer):
    date = DateField()

    class Meta:
        model = ComplexTimeSeries
        pandas_scatter_fields = ['units', 'parameter']
        pandas_header_fields = ['site']
        pandas_index_fields = ['date', 'type']
        exclude = ['id', 'flag']


if USE_LIST_SERIALIZERS:
    class NotUnstackableSerializer(ModelSerializer):
        class Meta:
            model = MultiTimeSeries
            list_serializer_class = PandasUnstackedSerializer
            # pandas_header_fields = Missing
            pandas_index_fields = ['series']
else:
    class NotUnstackableSerializer(ModelSerializer, PandasUnstackedSerializer):
        class Meta:
            model = MultiTimeSeries
            # pandas_header_fields = Missing
            pandas_index_fields = ['series']
