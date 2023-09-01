from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserSerializer
from recipes.models import (Recipe,
                            RecipeIngredient,
                            Tag,
                            Ingredient,
                            Favorite,
                            )
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('name', 'measurement_unit',)


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True,)
    author = CustomUserSerializer()
    ingredients = RecipeIngredientReadSerializer(
        many=True,
        source='r_i'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time'
                  )

    def get_image(self, obj):
        return obj.image.url

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (not request.user.is_anonymous
                and obj.favorites.filter(recipe=obj,
                                         user=request.user).exists()
                )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (not request.user.is_anonymous
                and obj.shopping_basket.filter(user=request.user).exists()
                )


class RecipeIngredientCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Кол-во ингридиента не может быть меньше 1.'
            )
        return value


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField()
    author = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'image', 'text',
                  'ingredients', 'cooking_time')

    def ingredients_create(self, instance, ingredients):
        bulk_list = []
        for ing in ingredients:
            bulk_list.append(
                RecipeIngredient(recipe=instance, ingredient_id=ing['id'],
                                 amount=ing['amount']))
        RecipeIngredient.objects.bulk_create(bulk_list,
                                             batch_size=len(ingredients))

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        self.ingredients_create(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            instance.r_i.all().delete()
            self.ingredients_create(instance, ingredients)
        tags_data = self.initial_data.pop("tags")
        instance.tags.set(tags_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance, context=self.context)
        return serializer.data

    def validate_cooking_time(self, data):
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) < 1:
            raise ValidationError(
                'Убедитесь, что время приготовления больше либо равно 1')
        return data


class FollowRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

    def get_image(self, obj):
        return obj.image.url


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()

    def get_recipes(self, obj):
        queryset = obj.author.recipe.all()
        limit = self.context.get('request').query_params.get('recipes_limit')

        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                raise ValueError('Неверно задан параметр количества рецептов')
        return FollowRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipe.all().count()


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id',)
