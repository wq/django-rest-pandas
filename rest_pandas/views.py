from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from django.conf import settings
from rest_framework.settings import perform_import

from .serializers import (
    SimpleSerializer, PandasSerializer
)

PANDAS_RENDERERS = getattr(settings, "PANDAS_RENDERERS", None)
if PANDAS_RENDERERS is None:
    PANDAS_RENDERERS = (
        "rest_pandas.renderers.PandasCSVRenderer",
        "rest_pandas.renderers.PandasTextRenderer",
        "rest_pandas.renderers.PandasJSONRenderer",
        "rest_pandas.renderers.PandasExcelRenderer",
        "rest_pandas.renderers.PandasOldExcelRenderer",
        "rest_pandas.renderers.PandasPNGRenderer",
        "rest_pandas.renderers.PandasSVGRenderer",
    )
    if "rest_pandas" in settings.INSTALLED_APPS:
        PANDAS_RENDERERS = (
            "rest_pandas.renderers.PandasHTMLRenderer",
        ) + PANDAS_RENDERERS

PANDAS_RENDERERS = perform_import(PANDAS_RENDERERS, "PANDAS_RENDERERS")


class PandasMixin(object):
    renderer_classes = PANDAS_RENDERERS
    pandas_serializer_class = PandasSerializer

    pagination_class = None

    def with_list_serializer(self, cls):
        meta = getattr(cls, 'Meta', object)
        if getattr(meta, 'list_serializer_class', None):
            return cls

        class SerializerWithListSerializer(cls):
            class Meta(meta):
                list_serializer_class = self.pandas_serializer_class

        return SerializerWithListSerializer


class PandasSimpleView(PandasMixin, APIView):
    """
    Simple (non-model) Pandas API view; override get_data
    with a function that returns a list of dicts.
    """
    serializer_class = SimpleSerializer

    def get_data(self, request, *args, **kwargs):
        return []

    def get(self, request, *args, **kwargs):
        data = self.get_data(request, *args, **kwargs)
        serializer_class = self.with_list_serializer(self.serializer_class)
        serializer = serializer_class(data, many=True)
        return Response(serializer.data)


class PandasView(PandasMixin, ListAPIView):
    """
    Pandas-capable model list view
    """
    def get_serializer_class(self, *args, **kwargs):
        cls = super(PandasView, self).get_serializer_class(*args, **kwargs)
        return self.with_list_serializer(cls)


class PandasViewSet(PandasMixin, ListModelMixin, GenericViewSet):
    """
    Pandas-capable model ViewSet (list only)
    """
    def get_serializer_class(self, *args, **kwargs):
        cls = super(PandasViewSet, self).get_serializer_class(*args, **kwargs)
        return self.with_list_serializer(cls)
