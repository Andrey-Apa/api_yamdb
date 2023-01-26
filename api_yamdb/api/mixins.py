from rest_framework import mixins, viewsets


class ListCreateDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):

    pass
