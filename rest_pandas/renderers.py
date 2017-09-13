from rest_framework.renderers import BaseRenderer, TemplateHTMLRenderer
from rest_framework import status
from tempfile import mkstemp
from pandas import DataFrame

try:
    # Python 2 (uses str)
    from StringIO import StringIO
except ImportError:
    # Python 3 (Python 2 equivalent uses unicode)
    from io import StringIO

import os
from io import BytesIO


RESPONSE_ERROR = (
    "Response data is a %s, not a DataFrame! "
    "Did you extend PandasMixin?"
)


class PandasBaseRenderer(BaseRenderer):
    """
    Renders DataFrames using their built in pandas implementation.
    Only works with serializers that return DataFrames as their data object.
    Uses a StringIO to capture the output of dataframe.to_[format]()
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'response' in renderer_context:
            status_code = renderer_context['response'].status_code
            if not status.is_success(status_code):
                return "Error: %s" % data.get('detail', status_code)

        if not isinstance(data, DataFrame):
            raise Exception(
                RESPONSE_ERROR % type(data).__name__
            )

        name = getattr(self, 'function', "to_%s" % self.format)
        if not hasattr(data, name):
            raise Exception("Data frame is missing %s property!" % name)

        self.init_output()
        args = self.get_pandas_args(data)
        kwargs = self.get_pandas_kwargs(data, renderer_context)
        self.render_dataframe(data, name, *args, **kwargs)
        return self.get_output()

    def render_dataframe(self, data, name, *args, **kwargs):
        function = getattr(data, name)
        function(*args, **kwargs)

    def init_output(self):
        self.output = StringIO()

    def get_output(self):
        return self.output.getvalue()

    def get_pandas_args(self, data):
        return [self.output]

    def get_pandas_kwargs(self, data, renderer_context):
        return {}


class PandasFileRenderer(PandasBaseRenderer):
    """
    Renderer for output formats that absolutely must use a file (i.e. Excel)
    """
    def init_output(self):
        file, filename = mkstemp(suffix='.' + self.format)
        self.filename = filename
        os.close(file)

    def get_pandas_args(self, data):
        return [self.filename]

    def get_output(self):
        file = open(self.filename, 'rb')
        result = file.read()
        file.close()
        os.unlink(self.filename)
        return result


class PandasHTMLRenderer(TemplateHTMLRenderer, PandasBaseRenderer):
    media_type = "text/html"
    format = "html"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        table = PandasBaseRenderer.render(
            self, data, accepted_media_type, renderer_context,
        )

        return TemplateHTMLRenderer.render(
            self, {'table': table}, accepted_media_type, renderer_context,
        )

    def get_template_context(self, data, renderer_context):
        view = renderer_context['view']
        request = renderer_context['request']

        data['name'] = view.get_view_name()
        data['description'] = view.get_view_description(html=True)
        data['url'] = request.path.replace('.html', '')
        full_path = request.get_full_path()
        if '?' in full_path:
            data['url_params'] = full_path[full_path.index('?'):]
        data['available_formats'] = [
            cls.format for cls in view.renderer_classes
            if cls.format != 'html'
        ]

        chart_type = view.pandas_serializer_class.wq_chart_type
        if chart_type:
            data['wq_chart_type'] = chart_type

        if hasattr(view, 'get_template_context'):
            data.update(view.get_template_context(data))

        return data

    def get_pandas_kwargs(self, data, renderer_context):
        return {
            'classes': 'ui-table table-stripe',
            'na_rep': '',
        }


class PandasCSVRenderer(PandasBaseRenderer):
    """
    Renders data frame as CSV
    """
    media_type = "text/csv"
    format = "csv"

    def get_pandas_kwargs(self, data, renderer_context):
        return {'encoding': self.charset}


class PandasTextRenderer(PandasCSVRenderer):
    """
    Renders data frame as CSV, but uses text/plain as media type
    """
    media_type = "text/plain"
    format = "txt"
    function = "to_csv"


class PandasJSONRenderer(PandasBaseRenderer):
    """
    Renders data frame as JSON
    """
    media_type = "application/json"
    format = "json"

    orient_choices = {
        'records-index',  # Unique to DRP
        'split',
        'records',
        'index',
        'columns',
        'values',
        'table',
    }
    default_orient = 'records-index'

    date_format_choices = {'epoch', 'iso'}
    default_date_format = 'iso'

    def get_pandas_kwargs(self, data, renderer_context):
        request = renderer_context['request']

        orient = request.GET.get('orient', '')
        if orient not in self.orient_choices:
            orient = self.default_orient

        date_format = request.GET.get('date_format', '')
        if date_format not in self.date_format_choices:
            date_format = self.default_date_format

        return {
            'orient': orient,
            'date_format': date_format,
        }

    def render_dataframe(self, data, name, *args, **kwargs):
        if kwargs.get('orient') == 'records-index':
            kwargs['orient'] = 'records'
            data.reset_index(inplace=True)
        return super(PandasJSONRenderer, self).render_dataframe(
            data, name, *args, **kwargs
        )


class PandasExcelRenderer(PandasFileRenderer):
    """
    Renders data frame as Excel (.xlsx)
    """
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # noqa
    format = "xlsx"
    function = "to_excel"


class PandasOldExcelRenderer(PandasFileRenderer):
    """
    Renders data frame as Excel (.xls)
    """
    media_type = "application/vnd.ms-excel"
    format = "xls"
    function = "to_excel"


class PandasImageRenderer(PandasBaseRenderer):
    """
    Renders dataframe using built-in plot() function
    """
    function = "plot"
    matplotlib_backend = 'Agg'

    def init_output(self):
        import matplotlib
        matplotlib.use(self.matplotlib_backend)
        import matplotlib.pyplot as plt
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def get_pandas_args(self, data):
        return []

    def get_pandas_kwargs(self, data, renderer_context):
        return {'ax': self.ax}

    def get_output(self):
        data = BytesIO()
        self.fig.savefig(data, format=self.format)
        return data.getvalue()


class PandasPNGRenderer(PandasImageRenderer):
    media_type = "image/png"
    format = "png"


class PandasSVGRenderer(PandasImageRenderer):
    media_type = "image/svg"
    format = "svg"
