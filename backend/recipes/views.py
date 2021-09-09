from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (exceptions, filters, mixins, permissions, viewsets)

from .filters import IngredientsFilter
from .models import Ingredients, Tag
from .serializers import IngredientsSerializer, TagsSerializer


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class =TagsSerializer
    permission_classes = [permissions.AllowAny]

