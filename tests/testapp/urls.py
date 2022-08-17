from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    NoModelView,
    FromFileView,
    TimeSeriesView,
    TimeSeriesNoIdView,
    TimeSeriesLabelsView,
    TimeSeriesMixedRendererView,
    TimeSeriesCustomCSVView,
    TimeSeriesMixinView,
    TimeSeriesNoMixinView,
    DjangoPandasView,
    TimeSeriesViewSet,
    MultiTimeSeriesView,
    MultiScatterView,
    MultiBoxplotView,
    ComplexTimeSeriesView,
    ComplexScatterView,
    ComplexBoxplotView,
    ComplexBoxplotExtraView,
    CustomIndexSeriesView,
)

router = DefaultRouter()
router.register("timeseries", TimeSeriesViewSet)

urlpatterns = [
    path("nomodel", NoModelView.as_view()),
    path("fromfile", FromFileView.as_view()),
    path("timeseries", TimeSeriesView.as_view()),
    path("timeseriesnoid", TimeSeriesNoIdView.as_view()),
    path("timeserieslabels", TimeSeriesLabelsView.as_view()),
    path("mixedrenderers", TimeSeriesMixedRendererView.as_view()),
    path("customcsv", TimeSeriesCustomCSVView.as_view()),
    path("mixin", TimeSeriesMixinView.as_view()),
    path("nomixin", TimeSeriesNoMixinView.as_view()),
    path("djangopandas", DjangoPandasView.as_view()),
    path("multitimeseries", MultiTimeSeriesView.as_view()),
    path("multiscatter", MultiScatterView.as_view()),
    path("multiboxplot", MultiBoxplotView.as_view()),
    path("complextimeseries", ComplexTimeSeriesView.as_view()),
    path("complexscatter", ComplexScatterView.as_view()),
    path("complexboxplot", ComplexBoxplotView.as_view()),
    path("complexboxplotextra", ComplexBoxplotExtraView.as_view()),
    path("customindex", CustomIndexSeriesView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    path("router/", include(router.urls)),
]
