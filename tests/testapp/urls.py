from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    NoModelView, FromFileView, TimeSeriesView, TimeSeriesNoIdView,
    TimeSeriesMixedRendererView, TimeSeriesMixinView, TimeSeriesNoMixinView,
    DjangoPandasView, TimeSeriesViewSet,
    MultiTimeSeriesView, MultiScatterView, MultiBoxplotView,
    ComplexTimeSeriesView, ComplexScatterView, ComplexBoxplotView,
    CustomIndexSeriesView,
)

router = DefaultRouter()
router.register('timeseries', TimeSeriesViewSet)

urlpatterns = [
    url(r'^nomodel$', NoModelView.as_view()),
    url(r'^fromfile$', FromFileView.as_view()),
    url(r'^timeseries$', TimeSeriesView.as_view()),
    url(r'^timeseriesnoid$', TimeSeriesNoIdView.as_view()),
    url(r'^mixedrenderers$', TimeSeriesMixedRendererView.as_view()),
    url(r'^mixin$', TimeSeriesMixinView.as_view()),
    url(r'^nomixin$', TimeSeriesNoMixinView.as_view()),
    url(r'^djangopandas$', DjangoPandasView.as_view()),
    url(r'^multitimeseries$', MultiTimeSeriesView.as_view()),
    url(r'^multiscatter$', MultiScatterView.as_view()),
    url(r'^multiboxplot$', MultiBoxplotView.as_view()),
    url(r'^complextimeseries$', ComplexTimeSeriesView.as_view()),
    url(r'^complexscatter$', ComplexScatterView.as_view()),
    url(r'^complexboxplot$', ComplexBoxplotView.as_view()),
    url(r'^customindex$', CustomIndexSeriesView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    url(r'^router/', include(router.urls)),
]
