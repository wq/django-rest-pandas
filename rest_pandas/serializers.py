from rest_framework import serializers
from pandas import DataFrame
from django.core.exceptions import ImproperlyConfigured


if hasattr(serializers, 'ListSerializer'):
    # Django REST Framework 3
    BaseSerializer = serializers.ListSerializer
    USE_LIST_SERIALIZERS = True
else:
    # Django REST Framework 2
    BaseSerializer = serializers.Serializer
    USE_LIST_SERIALIZERS = False


class PandasSerializer(BaseSerializer):
    """
    Transforms dataset into a dataframe and applies an index
    """
    read_only = True
    index_none_value = None

    def get_index(self, dataframe):
        return self.get_index_fields()

    def get_dataframe(self, data):
        dataframe = DataFrame(data)
        index = self.get_index(dataframe)
        if index:
            if self.index_none_value is not None:
                for key in index:
                    dataframe[key].fillna(self.index_none_value, inplace=True)
            dataframe.set_index(index, inplace=True)
        else:
            # Name auto-index column to ensure valid CSV output
            dataframe.index.name = 'row'
        return dataframe

    def transform_dataframe(self, dataframe):
        view = self.context.get('view', None)
        if view and hasattr(view, 'transform_dataframe'):
            return self.context['view'].transform_dataframe(dataframe)
        return dataframe

    @property
    def data(self):
        data = super(PandasSerializer, self).data
        if data:
            dataframe = self.get_dataframe(data)
            return self.transform_dataframe(dataframe)
        else:
            return DataFrame([])

    @property
    def model_serializer(self):
        if USE_LIST_SERIALIZERS:
            serializer = type(self.child)
        else:
            serializer = type(self)
        if serializer.__name__ == 'SerializerWithListSerializer':
            for base in serializer.__bases__:
                if not issubclass(base, PandasSerializer):
                    return base
        return serializer

    @property
    def model_serializer_meta(self):
        return getattr(self.model_serializer, 'Meta', object())

    def get_index_fields(self):
        """
        List of fields to use for index
        """
        default_fields = []
        if getattr(self.model_serializer_meta, 'model', None):
            default_fields = ['id']
        return self.get_meta_option('index', default_fields)

    def get_meta_option(self, name, default=None):
        meta_name = 'pandas_' + name
        value = getattr(self.model_serializer_meta, meta_name, None)

        if value is None:
            if default is not None:
                return default
            else:
                raise ImproperlyConfigured(
                    "%s should be specified on %s.Meta" %
                    (meta_name, self.model_serializer.__name__)
                )
        return value


class PandasUnstackedSerializer(PandasSerializer):
    """
    Pivots dataframe so commonly-repeating values are across the top in a
    multi-row header.  Intended for use with e.g. time series data, where the
    header includes metadata applicable to each time series.
    (Use with wq/chart.js' timeSeries() function)
    """
    index_none_value = '-'

    def get_index(self, dataframe):
        """
        Include header fields in initial index for later unstacking
        """
        return self.get_index_fields() + self.get_header_fields()

    def transform_dataframe(self, dataframe):
        """
        Unstack the dataframe so header fields are across the top.
        """
        dataframe.columns.name = ""

        for i in range(len(self.get_header_fields())):
            dataframe = dataframe.unstack()

        # Remove blank rows / columns
        dataframe = dataframe.dropna(
            axis=0, how='all'
        ).dropna(
            axis=1, how='all'
        )
        return dataframe

    def get_header_fields(self):
        """
        Series metadata fields for header (first few rows)
        """
        return self.get_meta_option('unstacked_header')


class PandasScatterSerializer(PandasSerializer):
    """
    Pivots dataframe into a format suitable for plotting two series
    against each other as x vs y on a scatter plot.
    (Use with wq/chart.js' scatter() function)
    """
    index_none_value = '-'

    def get_index(self, dataframe):
        """
        Include scatter & header fields in initial index for later unstacking
        """
        return (
            self.get_index_fields()
            + self.get_header_fields()
            + self.get_coord_fields()
        )

    def transform_dataframe(self, dataframe):
        """
        Unstack the dataframe so header consists of a composite 'value' header
        plus any other header fields.
        """
        coord_fields = self.get_coord_fields()
        header_fields = self.get_header_fields()
        for i in range(len(header_fields) + len(coord_fields)):
            dataframe = dataframe.unstack()

        # Compute new column headers
        columns = []
        for i in range(len(header_fields) + 1):
            columns.append([])

        for col in dataframe.columns:
            value_name = col[0]
            coord_names = list(col[1:len(coord_fields) + 1])
            header_names = list(col[len(coord_fields) + 1:])
            coord_name = ''
            for name in coord_names:
                if name != self.index_none_value:
                    coord_name += name + '-'
            coord_name += value_name
            columns[0].append(coord_name)
            for i, header_name in enumerate(header_names):
                columns[1 + i].append(header_name)

        dataframe.columns = columns
        dataframe.columns.names = [''] + header_fields

        # Remove blank columns
        dataframe = dataframe.dropna(axis=1, how='all')

        # Remove any rows that don't have data for all columns (e.g. x & y)
        dataframe = dataframe.dropna(axis=0, how='any')
        return dataframe

    def get_coord_fields(self):
        """
        Fields that will be collapsed into a single header with the name of
        each coordinate.
        """
        return self.get_meta_option('scatter_coord')

    def get_header_fields(self):
        """
        Other header fields, if any
        """
        return self.get_meta_option('scatter_header', [])


class SimpleSerializer(serializers.Serializer):
    """
    Simple serializer for non-model (simple) views
    """

    # DRF 3
    def to_representation(self, obj):
        return obj

    # DRF 2
    def to_native(self, obj):
        return obj
