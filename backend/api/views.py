from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Tag, Recipe, RecipeIngredient, Ingredient
from api.serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, FollowSerializer, RecipeCreateSerializer
from api.permissions import IsAuthorOrReadOnlyPermission

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeReadSerializer

    # def get_permissions(self):
    #     if self.action == 'DELETE':
    #         return (IsAuthorOrReadOnlyPermission(),)
    #     return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowView(APIView):

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
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.follower.all()
