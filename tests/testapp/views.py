from rest_pandas import PandasSimpleView, PandasView, PandasViewSet
from .models import TimeSeries


class NoModelView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return [
            {'x': 5, 'y': 7},
            {'x': 3, 'y': 2},
            {'x': 8, 'y': 6},
            {'x': 5, 'y': 4},
        ]


class TimeSeriesView(PandasView):
    model = TimeSeries


class TimeSeriesViewSet(PandasViewSet):
    model = TimeSeries
