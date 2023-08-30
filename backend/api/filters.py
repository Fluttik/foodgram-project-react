import django_filters
from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Tag, Recipe, Favorite, ShoppingBasket

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
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)

    def filter_is_favorited(self, queryset, name, value):
        if value == 1:
            favorite_recipes_ids = Favorite.objects.filter(
                user=self.request.user).values('recipe_id')
            return queryset.filter(pk__in=favorite_recipes_ids)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            basket_recipes_ids = ShoppingBasket.objects.filter(
                user_id=self.request.user.id).values('recipe_id')
            return queryset.filter(pk__in=basket_recipes_ids)
        return queryset
