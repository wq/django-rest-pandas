from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from django.conf import settings
from rest_framework.settings import perform_import

from .serializers import PandasSimpleSerializer, PandasSerializer

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

PANDAS_RENDERERS = perform_import(PANDAS_RENDERERS, "PANDAS_RENDERERS")


class PandasSimpleView(APIView):
    """
    Simple (non-model) Pandas API view; override get_data
    with a function that returns a list of dicts.
    """
    serializer_class = PandasSimpleSerializer
    renderer_classes = PANDAS_RENDERERS

    def get_data(self, request, *args, **kwargs):
        return []

    def get(self, request, *args, **kwargs):
        data = self.get_data(request, *args, **kwargs)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)


class PandasView(ListAPIView):
    """
    Pandas-capable model list view
    """
    model_serializer_class = PandasSerializer
    renderer_classes = PANDAS_RENDERERS
    paginate_by = None


class PandasViewSet(ListModelMixin, GenericViewSet):
    """
    Pandas-capable model ViewSet (list only)
    """
    model_serializer_class = PandasSerializer
    renderer_classes = PANDAS_RENDERERS
    paginate_by = None
