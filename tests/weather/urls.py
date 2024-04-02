from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import WeatherView

urlpatterns = [
    path("weather", WeatherView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
