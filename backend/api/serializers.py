from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug',)
        read_only_fields = ('name', 'color', 'slug',)
