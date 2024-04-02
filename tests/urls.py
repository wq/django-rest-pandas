from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path("", include("tests.testapp.urls")),
    path("", include("tests.weather.urls")),
    path("admin", admin.site.urls),
]
