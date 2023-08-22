from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from djoser.serializers import UserSerializer
from recipes.models import Recipe, RecipeIngredient, Tag, Ingredient, Favorite, ShoppingBasket

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit',)
        read_only_fields = ('name', 'measurement_unit',)


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id',  'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True,)
    author = UserSerializer()
    ingedients = RecipeIngredientReadSerializer(
        many=True,
        source='recipe_ingredients'
    )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_card = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingedients',
                #   'is_favorited',
                #   'is_in_shopping_card',
                  'name',
                  'text',
                  'cooking_time'
                  )

    # def get_is_favorited(self, obj):
    #     request = self.context.get('request')
    #     if request.user.is_anonymous:
    #         return False
    #     return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    # def get_is_in_shopping_card(self, obj):
    #     request = self.context.get('request')
    #     if request.user.is_anonymous:
    #         return False
    #     return ShoppingBasket.objects.filter(
    #         recipe=obj, user=request.user).exists


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
    # image = Base64ImageField(max_length=None, use_url=True)
    author = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text',
                  'ingredients', 'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        bulk_list = []
        for ing in ingredients:
            bulk_list.append(
                RecipeIngredient(recipe=instance, ingredient_id=ing['id'],
                                 amount=ing['amount']))
        print(bulk_list)
        RecipeIngredient.objects.bulk_create(bulk_list,
                                             batch_size=len(ingredients))
        return instance

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        return serializer.data


class FollowRecipeSerializer(serializers.ModelSerializer):
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            # "image",
            "cooking_time",
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    recipe_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            'recipe',
            'recipe_count',
        )

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()

    def get_recipe(self, obj):
        queryset = obj.author.recipe.all().order_by('-pub_date')
        return FollowRecipeSerializer(queryset, many=True).data

    def get_recipe_count(self, obj):
        return obj.author.recipe.all().count()


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id',)
