import django_filters
from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Tag, Recipe

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
         field_name='tags__slug',
         to_field_name='slug',
         queryset=Tag.objects.all(),
     )
    author = django_filters.ModelChoiceFilter(
         queryset=User.objects.all()
     )

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
