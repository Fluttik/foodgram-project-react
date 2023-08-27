import django_filters
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Tag, Ingredient

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)

# class CharFiterInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
#     pass

# class RecipeFilter(django_filters.FilterSet):
#     tags = CharFiterInFilter(field_name='tags__slug', to_field_name='slug')

#     class Meta:
#         model = Recipe
#         fields = ['tags']


class RecipeFilter(django_filters.FilterSet):
    # tags = django_filters.MultipleChoiceFilter(
    #     field_name='tags__slug',
    #     # to_field_name='slug',
    #     queryset=Tag.objects.all(),
    # )
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = django_filters.BooleanFilter(method='filter_favorited')

    def filter_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            print('******')
            return queryset.filter(recipe_favorites_user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited')
