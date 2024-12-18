from django.urls import path, include
from recipes.api.v1 import views as recipe_views

# Version 1 API endpoints
v1_patterns = [
    path('recipes/', recipe_views.RecipeListCreateView.as_view(), name='recipe-list'),
    path('recipes/<slug:slug>/', recipe_views.RecipeDetailView.as_view(), name='recipe-detail'),
]

urlpatterns = [
    path('api/v1/', include((v1_patterns, 'v1')), name='api-v1'),
]