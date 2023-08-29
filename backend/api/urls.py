from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views import (TagsViewSet,
                       IngredientViewSet,
                       FollowView,
                       FollowsView,
                       RecipeViewSet)

router = SimpleRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet, basename='recipe-list')

urlpatterns = [
    path('users/subscriptions/', FollowsView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/<int:id>/subscribe/', FollowView.as_view()),
]
