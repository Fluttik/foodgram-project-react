from django.shortcuts import render
from rest_framework import viewsets
from recipes.models import Tag, Recipe, RecipeIngredient, Ingredient
from api.serializers import TagSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
