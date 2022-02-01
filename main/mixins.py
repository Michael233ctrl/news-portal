from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet


class BulkUpdateSerializerMixin(Serializer):
    """
    Mixin to be used with BulkUpdateListSerializer & BulkUpdateRouteMixin
    that adds the ID back to the internal value from the raw input data so
    that it's included in the validated data.
    """

    def passes_test(self):
        # Must be an update method for the ID to be added to validated data
        test = self.context['request'].method in ('PUT', 'PATCH')
        test &= self.context.get('bulk_update', False)

        return test

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        if self.passes_test():
            ret['id'] = self.fields['id'].get_value(data)

        return ret


class BulkUpdateRouteMixin(ModelViewSet):
    """
    Mixin that adds a `bulk_update` API route to a view set. To be used
    with BulkUpdateSerializerMixin & BulkUpdateListSerializer.
    """

    def get_object(self):
        # Override to return None if the lookup_url_kwargs is not present.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            return super().get_object()
        return

    def get_serializer(self, *args, **kwargs):
        # Initialize serializer with `many=True` if the data passed
        # to the serializer is a list.
        if self.request.method in ('PUT', 'PATCH'):
            data = kwargs.get('data', None)
            kwargs['many'] = isinstance(data, list)
        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        # Add `bulk_update` flag to the serializer context so that
        # the id field can be added back to the validated data through
        # `to_internal_value()`
        context = super().get_serializer_context()
        if self.action == 'bulk_update':
            context['bulk_update'] = True
        return context

    @action(detail=False, methods=['put'], url_name='bulk_update')
    def bulk_update(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset,
            data=request.data,
            many=True,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
