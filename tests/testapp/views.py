from rest_pandas import (
    PandasMixin, PandasSimpleView, PandasView, PandasViewSet,
    PandasUnstackedSerializer, PandasScatterSerializer, PandasBoxplotSerializer
)
from rest_framework import renderers
from rest_framework.generics import ListAPIView
from rest_pandas import renderers as pandas_renderers
from .models import (
    TimeSeries, MultiTimeSeries, ComplexTimeSeries, CustomIndexSeries,
)
from .serializers import (
    TimeSeriesSerializer, TimeSeriesNoIdSerializer,
    MultiTimeSeriesSerializer,
    ComplexTimeSeriesSerializer, ComplexScatterSerializer,
    ComplexBoxplotSerializer, ComplexBoxplotExtraSerializer,
    CustomIndexSeriesSerializer,
)
from .renderers import CustomCSVRenderer
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

    def get_template_context(self, data):
        return {'name': data['name'] + ' Custom'}

    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            return self.get_view_name()
        else:
            return None


class TimeSeriesNoIdView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesNoIdSerializer


class TimeSeriesMixedRendererView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer

    renderer_classes = [
         renderers.BrowsableAPIRenderer,
         pandas_renderers.PandasCSVRenderer,
         renderers.JSONRenderer,
    ]


class TimeSeriesCustomCSVView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer

    renderer_classes = [
         CustomCSVRenderer,
    ]

    def transform_dataframe(self, df):
        df['date'] = df['date'].astype('datetime64')
        return df


class TimeSeriesViewSet(PandasViewSet):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer


class TimeSeriesMixinView(PandasMixin, ListAPIView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer
    renderer_classes = [
        pandas_renderers.PandasCSVRenderer
    ]


class TimeSeriesNoMixinView(ListAPIView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer
    renderer_classes = [
        pandas_renderers.PandasCSVRenderer
    ]


class DjangoPandasView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return TimeSeries.objects.to_timeseries(
            index='date',
        )


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


class ComplexBoxplotExtraView(PandasView):
    queryset = ComplexTimeSeries.objects.all()
    serializer_class = ComplexBoxplotExtraSerializer
    pandas_serializer_class = PandasBoxplotSerializer


class CustomIndexSeriesView(PandasView):
    queryset = CustomIndexSeries.objects.all()
    serializer_class = CustomIndexSeriesSerializer
