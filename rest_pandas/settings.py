from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


if hasattr(settings, "PANDAS_RENDERERS"):
    raise ImproperlyConfigured(
        'PANDAS_RENDERERS is now REST_PANDAS["RENDERERS"]'
    )


REST_PANDAS = getattr(settings, "REST_PANDAS", None) or {}

RENDERERS = REST_PANDAS.get(
    "RENDERERS",
    (
        "wq.db.rest.renderers.HTMLRenderer"
        if getattr(settings, "WQ_APP_TEMPLATE", None)
        else "rest_pandas.renderers.PandasHTMLRenderer",
        "rest_pandas.renderers.PandasCSVRenderer",
        "rest_pandas.renderers.PandasTextRenderer",
        "rest_pandas.renderers.PandasJSONRenderer",
        "rest_pandas.renderers.PandasExcelRenderer",
        "rest_pandas.renderers.PandasOldExcelRenderer",
        "rest_pandas.renderers.PandasPNGRenderer",
        "rest_pandas.renderers.PandasSVGRenderer",
    ),
)

APPLY_FIELD_LABELS = REST_PANDAS.get("APPLY_FIELD_LABELS", True)
INDEX_NONE_VALUE = REST_PANDAS.get("INDEX_NONE_VALUE", None)
