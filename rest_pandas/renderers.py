from rest_framework.renderers import BaseRenderer
from rest_framework import status
from tempfile import mkstemp

try:
    # Python 2 (uses str)
    from StringIO import StringIO
except ImportError:
    # Python 3 (Python 2 equivalent uses unicode)
    from io import StringIO

import os


class PandasBaseRenderer(BaseRenderer):
    """
    Renders DataFrames using their built in Pandas implementation.
    Only works with serializers that return DataFrames as their data object.
    Uses a StringIO to capture the output of dataframe.to_[format]()
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'response' in renderer_context:
            status_code = renderer_context['response'].status_code
            if not status.is_success(status_code):
                return "Error: %s" % data.get('detail', status_code)

        name = getattr(self, 'function', "to_%s" % self.format)
        function = getattr(data, name, None)
        if not function:
            raise Exception("Data frame is missing %s property!" % name)
        self.init_output()
        args = self.get_pandas_args(data)
        kwargs = self.get_pandas_kwargs(data)
        function(*args, **kwargs)
        return self.get_output()

    def init_output(self):
        self.output = StringIO()

    def get_output(self):
        return self.output.getvalue()

    def get_pandas_args(self, data):
        return [self.output]

    def get_pandas_kwargs(self, data):
        return {}


class PandasFileRenderer(PandasBaseRenderer):
    """
    Renderer for output formats that absolutely must use a file (i.e. Excel)
    """
    def init_output(self):
        file, filename = mkstemp(suffix='.' + self.format)
        self.filename = filename

    def get_pandas_args(self, data):
        return [self.filename]

    def get_output(self):
        result = open(self.filename).read()
        os.unlink(self.filename)
        return result


class PandasCSVRenderer(PandasBaseRenderer):
    """
    Renders data frame as CSV
    """
    media_type = "text/csv"
    format = "csv"

    def get_pandas_kwargs(self, data):
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

    def get_pandas_kwargs(self, data):
        return {
            'orient': 'index',
            'date_format': 'iso',
        }


class PandasExcelRenderer(PandasFileRenderer):
    """
    Renders data frame as Excel (.xlsx)
    """
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

    def init_output(self):
        import matplotlib.pyplot as plt
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def get_pandas_args(self, data):
        return []

    def get_pandas_kwargs(self, data):
        return {'ax': self.ax}

    def get_output(self):
        data = StringIO()
        self.fig.savefig(data, format=self.format)
        return data.getvalue()


class PandasPNGRenderer(PandasImageRenderer):
    media_type = "image/png"
    format = "png"


class PandasSVGRenderer(PandasImageRenderer):
    media_type = "image/svg"
    format = "svg"
