from rest_framework import mixins
from rest_framework.generics import GenericAPIView


class ListUpdateAPIView(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing and updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateCreateAPIView(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          GenericAPIView):
    """
    Concrete view for creating and updating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
