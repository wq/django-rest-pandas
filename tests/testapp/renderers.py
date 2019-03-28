from rest_pandas.renderers import PandasCSVRenderer


class CustomCSVRenderer(PandasCSVRenderer):
    def get_pandas_kwargs(self, data, renderer_context):
        kwargs = super(CustomCSVRenderer, self).get_pandas_kwargs(
            data, renderer_context
        )
        kwargs['date_format'] = '%d-%m-%Y'
        return kwargs
