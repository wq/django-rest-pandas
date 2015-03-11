from rest_pandas import PandasSimpleView, PandasView, PandasViewSet
from .models import TimeSeries
from .serializers import TimeSeriesSerializer


class NoModelView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return [
            {'x': 5, 'y': 7},
            {'x': 3, 'y': 2},
            {'x': 8, 'y': 6},
            {'x': 5, 'y': 4},
        ]


class TimeSeriesView(PandasView):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer

    def transform_dataframe(self, df):
        df['date'] = df['date'].astype('datetime64[D]')
        return df


class TimeSeriesViewSet(PandasViewSet):
    queryset = TimeSeries.objects.all()
    serializer_class = TimeSeriesSerializer
