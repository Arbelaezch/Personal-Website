from django.urls import path
from recipes.api.v1 import views as recipe_views


urlpatterns = [
    path('v1/recipes/', recipe_views.RecipeListCreateView.as_view(), name='recipe-list'),
    path('v1/recipes/<slug:slug>/', recipe_views.RecipeDetailView.as_view(), name='recipe-detail'),
]