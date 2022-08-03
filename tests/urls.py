from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path("", include("tests.testapp.urls")),
    path("admin", admin.site.urls),
]
