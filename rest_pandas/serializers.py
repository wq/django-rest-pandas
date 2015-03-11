from rest_framework import serializers
from pandas import DataFrame


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
        model_serializer = getattr(self, 'child', self)
        if getattr(model_serializer.Meta, 'model', None):
            return ['id']
        return None

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
