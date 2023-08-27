import django_filters
from django.contrib.auth import get_user_model

from recipes.models import Ingredient

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
