from rest_framework import serializers
from pandas import DataFrame
from django.core.exceptions import ImproperlyConfigured
import datetime


class PandasSerializer(serializers.ListSerializer):
    """
    Transforms dataset into a dataframe and applies an index
    """
    read_only = True
    index_none_value = None
    wq_chart_type = None

    def get_index(self, dataframe):
        return self.get_index_fields()

    def get_dataframe(self, data):
        dataframe = DataFrame(data)
        index = self.get_index(dataframe)
        if index:
            if self.index_none_value is not None:
                for key in index:
                    try:
                        dataframe[key].fillna(
                            self.index_none_value, inplace=True
                        )
                    except ValueError:
                        pass
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
        data = super(serializers.ListSerializer, self).data
        if isinstance(data, DataFrame) or data:
            dataframe = self.get_dataframe(data)
            return self.transform_dataframe(dataframe)
        else:
            return DataFrame([])

    def to_representation(self, data):
        if isinstance(data, DataFrame):
            return data
        return super(PandasSerializer, self).to_representation(data)

    @property
    def model_serializer(self):
        serializer = type(self.child)
        if serializer.__name__ == 'SerializerWithListSerializer':
            return serializer.__bases__[0]
        return serializer

    @property
    def model_serializer_meta(self):
        return getattr(self.model_serializer, 'Meta', object())

    def get_index_fields(self):
        """
        List of fields to use for index
        """
        index_fields = self.get_meta_option('index', [])
        if index_fields:
            return index_fields

        model = getattr(self.model_serializer_meta, 'model', None)
        if model:
            pk_name = model._meta.pk.name
            if pk_name in self.child.get_fields():
                return [pk_name]

        return []

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
    wq_chart_type = 'timeSeries'

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
    wq_chart_type = 'scatter'

    def get_index(self, dataframe):
        """
        Include scatter & header fields in initial index for later unstacking
        """
        return (
            self.get_index_fields() +
            self.get_header_fields() +
            self.get_coord_fields()
        )

    def transform_dataframe(self, dataframe):
        """
        Unstack the dataframe so header consists of a composite 'value' header
        plus any other header fields.
        """
        coord_fields = self.get_coord_fields()
        header_fields = self.get_header_fields()

        # Remove any pairs that don't have data for both x & y
        for i in range(len(coord_fields)):
            dataframe = dataframe.unstack()
        dataframe = dataframe.dropna(axis=1, how='all')
        dataframe = dataframe.dropna(axis=0, how='any')

        # Unstack series header
        for i in range(len(header_fields)):
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


class PandasBoxplotSerializer(PandasSerializer):
    """
    Compute boxplot statistics on dataframe columns, creating a new unstacked
    dataframe where each row describes a boxplot.
    (Use with wq/chart.js' boxplot() function)
    """
    index_none_value = '-'
    wq_chart_type = 'boxplot'

    def get_index(self, dataframe):
        group_field = self.get_group_field()
        date_field = self.get_date_field()
        header_fields = self.get_header_fields()

        if date_field:
            group_fields = [date_field, group_field]
        else:
            group_fields = [group_field]
        return group_fields + header_fields

    def transform_dataframe(self, dataframe):
        """
        Use matplotlib to compute boxplot statistics on e.g. timeseries data.
        """
        grouping = self.get_grouping(dataframe)
        group_field = self.get_group_field()
        header_fields = self.get_header_fields()

        if "series" in grouping:
            # Unstack so each series is a column
            for i in range(len(header_fields) + 1):
                dataframe = dataframe.unstack()

        groups = {
            col: dataframe[col]
            for col in dataframe.columns
        }

        if "year" in grouping:
            interval = "year"
        elif "month" in grouping:
            interval = "month"
        else:
            interval = None

        # Compute stats for each column, potentially grouped by year
        all_stats = []
        for header, series in groups.items():
            if interval:
                series_stats = self.boxplots_for_interval(series, interval)
            else:
                interval = None
                series_stats = [self.compute_boxplot(series)]

            series_infos = []
            for series_stat in series_stats:
                series_info = {}
                if isinstance(header, tuple):
                    value_name = header[0]
                    col_values = header[1:]
                else:
                    value_name = header
                    col_values = []
                col_names = zip(dataframe.columns.names[1:], col_values)
                for col_name, value in col_names:
                    series_info[col_name] = value
                for stat_name, val in series_stat.items():
                    if stat_name == interval:
                        series_info[stat_name] = val
                    else:
                        series_info[value_name + '-' + stat_name] = val
                series_infos.append(series_info)
            all_stats += series_infos

        dataframe = DataFrame(all_stats)
        if 'series' in grouping:
            index = header_fields + [group_field]
            unstack = len(header_fields)
            if interval:
                index = [interval] + index
                unstack += 1
        else:
            index = [interval]
            unstack = 0

        dataframe.set_index(index, inplace=True)
        dataframe.columns.name = ''
        for i in range(unstack):
            dataframe = dataframe.unstack()

        # Remove blank columns
        dataframe = dataframe.dropna(axis=1, how='all')
        return dataframe

    def get_grouping(self, dataframe):
        request = self.context.get('request', None)
        datasets = len(dataframe.columns)
        if request:
            group = request.GET.get('group', None)
            if group:
                return group
        return default_grouping(datasets, self.get_date_field())

    def boxplots_for_interval(self, series, interval):
        def get_interval_name(date):
            if isinstance(date, tuple):
                date = date[0]
            if hasattr(date, 'count') and date.count('-') == 2:
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
            return getattr(date, interval)

        interval_stats = []
        groups = series.groupby(get_interval_name).groups
        for interval_name, group in groups.items():
            stats = self.compute_boxplot(series[group])
            stats[interval] = interval_name
            interval_stats.append(stats)
        return interval_stats

    def compute_boxplot(self, series):
        """
        Compute boxplot for given pandas Series.
        """
        from matplotlib.cbook import boxplot_stats
        series = series[series.notnull()]
        if len(series.values) == 0:
            return {}
        stats = boxplot_stats(list(series.values))[0]
        stats['count'] = len(series.values)
        stats['fliers'] = "|".join(map(str, stats['fliers']))
        return stats

    def get_group_field(self):
        """
        Categorical field to group datasets by.
        """
        return self.get_meta_option('boxplot_group')

    def get_date_field(self):
        """
        Date field to group datasets by year or month.
        """
        return self.get_meta_option('boxplot_date', False)

    def get_header_fields(self):
        """
        Additional series metadata for boxplot column headers
        """
        return self.get_meta_option('boxplot_header', [])


class SimpleSerializer(serializers.Serializer):
    """
    Simple serializer for non-model (simple) views
    """
    def to_representation(self, obj):
        return obj


def default_grouping(datasets, date_field=None):
    """
    Heuristic for default boxplot grouping
    """
    if datasets > 20 and date_field:
        # Group all data by year
        return "year"
    elif datasets > 10 or not date_field:
        # Compare series but don't break down by year
        return "series"
    else:
        # 10 or fewer datasets, break down by both series and year
        return "series-year"
