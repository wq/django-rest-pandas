from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import NoModelView, TimeSeriesView, TimeSeriesViewSet

router = DefaultRouter()
router.register('timeseries', TimeSeriesViewSet)

urlpatterns = patterns('',
    url(r'^nomodel$', NoModelView.as_view()),  # noqa
    url(r'^timeseries$', TimeSeriesView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += patterns('',
    url(r'^router/', include(router.urls)),  # noqa
)
