import django_filters
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Tag

User = get_user_model()

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
    
    class Meta:
        model = Recipe
        fields = ('author',)
