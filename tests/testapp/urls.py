from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from .views import NoModelView, TimeSeriesView, TimeSeriesViewSet

router = DefaultRouter()
router.register('timeseries', TimeSeriesViewSet)

urlpatterns = patterns('',
    url(r'^nomodel', NoModelView.as_view()),
    url(r'^timeseries', TimeSeriesView.as_view()),
    url(r'^router/', include(router.urls)),
)
