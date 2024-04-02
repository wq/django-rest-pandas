from rest_pandas import PandasView, PandasUnstackedSerializer
from .models import Weather
from .serializers import WeatherSerializer


class WeatherView(PandasView):
    queryset = Weather.objects.select_related("station")
    serializer_class = WeatherSerializer
    pandas_serializer_class = PandasUnstackedSerializer
