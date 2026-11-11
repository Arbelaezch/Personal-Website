from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Recipe
from .serializers import RecipeSerializer


# Read-only on purpose: the public API (used by the family-food frontend) only ever reads.
# Recipes are created and edited in the Django admin. Only published recipes are exposed.

class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'rating']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'rating', 'title']
    ordering = ['-created_at']  # Default ordering


class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeSerializer
    lookup_field = 'slug'  # Use slug instead of pk for lookups
