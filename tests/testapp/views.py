from rest_pandas import (
    PandasSimpleView, PandasView, PandasViewSet,
    PandasUnstackedSerializer, PandasScatterSerializer, PandasBoxplotSerializer
)
from .models import TimeSeries, MultiTimeSeries, ComplexTimeSeries
from .serializers import (
    TimeSeriesSerializer, MultiTimeSeriesSerializer,
    ComplexTimeSeriesSerializer, ComplexScatterSerializer,
    ComplexBoxplotSerializer,
)
import pandas as pd


class NoModelView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return [
            {'x': 5, 'y': 7},
            {'x': 3, 'y': 2},
            {'x': 8, 'y': 6},
            {'x': 5, 'y': 4},
        ]


class FromFileView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('tests/data.csv')


class TimeSeriesView(PandasView):
    """
    A simple time series view.
    """
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer

    def transform_dataframe(self, df):
        df['date'] = df['date'].astype('datetime64[D]')
        return df

    def get_template_context(self, data):
        return {'name': data['name'] + ' Custom'}


class TimeSeriesViewSet(PandasViewSet):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer


class MultiTimeSeriesView(PandasView):
    """
    Multiple time series.
    """
    queryset = MultiTimeSeries.objects.all()
    serializer_class = MultiTimeSeriesSerializer
    pandas_serializer_class = PandasUnstackedSerializer


class MultiScatterView(PandasView):
    queryset = MultiTimeSeries.objects.all()
    serializer_class = MultiTimeSeriesSerializer
    pandas_serializer_class = PandasScatterSerializer


class MultiBoxplotView(PandasView):
    queryset = MultiTimeSeries.objects.all()
    serializer_class = MultiTimeSeriesSerializer
    pandas_serializer_class = PandasBoxplotSerializer


class ComplexTimeSeriesView(PandasView):
    queryset = ComplexTimeSeries.objects.all()
    serializer_class = ComplexTimeSeriesSerializer
    pandas_serializer_class = PandasUnstackedSerializer


class ComplexScatterView(PandasView):
    queryset = ComplexTimeSeries.objects.all()
    serializer_class = ComplexScatterSerializer
    pandas_serializer_class = PandasScatterSerializer


class ComplexBoxplotView(PandasView):
    queryset = ComplexTimeSeries.objects.all()
    serializer_class = ComplexBoxplotSerializer
    pandas_serializer_class = PandasBoxplotSerializer
