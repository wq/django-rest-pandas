from .renderers import PandasBaseRenderer
try:
    from rest_framework.views import APIView
except ImportError as e:
    if 'APIView' in e.msg:
        raise ImportError(
            "Try importing rest_pandas before rest_framework.views"
        )
    else:
        raise
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from django.conf import settings
from rest_framework.settings import perform_import

from .serializers import (
    SimpleSerializer, PandasSerializer
)

DEFAULT_TEMPLATE = False
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
        DEFAULT_TEMPLATE = True
        PANDAS_RENDERERS = (
            "rest_pandas.renderers.PandasHTMLRenderer",
        ) + PANDAS_RENDERERS

PANDAS_RENDERERS = perform_import(PANDAS_RENDERERS, "PANDAS_RENDERERS")


class PandasMixin(object):
    pandas_serializer_class = PandasSerializer

    def with_list_serializer(self, cls):
        meta = getattr(cls, 'Meta', object)
        if getattr(meta, 'list_serializer_class', None):
            return cls

        class SerializerWithListSerializer(cls):
            class Meta(meta):
                list_serializer_class = self.pandas_serializer_class

        return SerializerWithListSerializer

    def get_serializer_class(self):

        # c.f rest_framework.generics.GenericAPIView
        # (not using super() since this is a mixin class)
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        renderer = self.request.accepted_renderer
        if hasattr(renderer, 'get_default_renderer'):
            # BrowsableAPIRenderer
            renderer = renderer.get_default_renderer(self)

        if isinstance(renderer, PandasBaseRenderer):
            return self.with_list_serializer(self.serializer_class)
        else:
            return self.serializer_class

    def get_pandas_filename(self, request, format):
        return None

    def get_pandas_headers(self, request):
        format = request.accepted_renderer.format
        filename = self.get_pandas_filename(request, format)
        if not filename:
            return {}

        extension = '.' + format
        if not filename.endswith(extension):
            filename += extension

        return {
            'Content-Disposition': 'attachment; filename="{}"'.format(
                filename
            )
        }

    def update_pandas_headers(self, response):
        headers = self.get_pandas_headers(self.request)
        for key, val in headers.items():
            response[key] = val
        return response


class PandasViewBase(PandasMixin):
    renderer_classes = PANDAS_RENDERERS
    pagination_class = None
    if DEFAULT_TEMPLATE:
        template_name = 'rest_pandas.html'


class PandasSimpleView(PandasViewBase, APIView):
    """
    Simple (non-model) Pandas API view; override get_data
    with a function that returns a list of dicts.
    """
    serializer_class = SimpleSerializer

    def get_data(self, request, *args, **kwargs):
        return []

    def get(self, request, *args, **kwargs):
        data = self.get_data(request, *args, **kwargs)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data, many=True)
        response = Response(serializer.data)
        return self.update_pandas_headers(response)


class PandasView(PandasViewBase, ListAPIView):
    """
    Pandas-capable model list view
    """

    def list(self, request, *args, **kwargs):
        response = super(PandasView, self).list(request, *args, **kwargs)
        return self.update_pandas_headers(response)


class PandasViewSet(PandasViewBase, ListModelMixin, GenericViewSet):
    """
    Pandas-capable model ViewSet (list only)
    """
    def list(self, request, *args, **kwargs):
        response = super(PandasViewSet, self).list(request, *args, **kwargs)
        return self.update_pandas_headers(response)
