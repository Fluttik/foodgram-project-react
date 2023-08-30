from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Tag, Recipe, Ingredient, Favorite, ShoppingBasket
from api.serializers import (TagSerializer,
                             IngredientSerializer,
                             RecipeReadSerializer,
                             FollowSerializer,
                             RecipeCreateSerializer,
                             FollowRecipeSerializer
                             )
from api.permissions import IsAuthorOrReadOnlyPermission
from api.filters import IngredientFilter, RecipeFilter
from api.utils import create_pdf

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов.
    get_queryset в зависимости от тела запроса фильтрует queryset
    favorite используется для добавления и удаления рецепта
    из избранного(POST, DELETE)
    shopping_cart используется для добавления и удаления рецепта
    из списка покупок (POST, DELETE)
    download_shopping_cart на основе списка покупок создает pdf файл
    с помощью функции pdf_create
    """
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = Recipe.objects.all()

        # if self.request.GET.get('is_favorited'):
        #     favorite_recipes_ids = Favorite.objects.filter(
        #         user_id=self.request.user.id).values('recipe_id')
        #     return queryset.filter(pk__in=favorite_recipes_ids)

        # if self.request.GET.get('is_in_shopping_cart'):
        #     basket_recipes_ids = ShoppingBasket.objects.filter(
        #         user_id=self.request.user.id).values('recipe_id')
        #     return queryset.filter(pk__in=basket_recipes_ids)
        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            context = {"request": request}
            serializer = FollowRecipeSerializer(recipe, context=context)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        targ = Favorite.objects.filter(user=request.user, recipe__id=pk)
        if targ.exists():
            targ.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            ShoppingBasket.objects.create(user=request.user, recipe=recipe)
            context = {"request": request}
            serializer = FollowRecipeSerializer(recipe, context=context)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        targ = ShoppingBasket.objects.filter(user=request.user, recipe__id=pk)
        if targ.exists():
            targ.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = request.user.shopping_basket.values(
            'recipe__r_i__ingredient__name',
            'recipe__r_i__ingredient__measurement_unit'
        ).annotate(amount=Sum('recipe__r_i__amount'))
        path_file = create_pdf(ingredients)
        response = FileResponse(open(path_file, 'rb'),
                                content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        return response


class FollowView(APIView):
    """Вьюсет для подписок.
    реализует функции подписки и отписки
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.follower.filter(author=author).exists():
            return Response(
                {"errors": "Вы уже подписаны на автора"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FollowSerializer(
            request.user.follower.create(author=author),
            context={"request": request},
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.follower.filter(author=author).exists():
            request.user.follower.filter(
                author=author
            ).delete()
            return Response({"Success": "Вы отпписались от пользователя"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Автор отсутсвует в списке подписок"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FollowsView(generics.ListAPIView):
    """Вьюсет для отображения подписок."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.follower.all()
