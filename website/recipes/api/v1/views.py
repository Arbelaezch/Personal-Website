from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Recipe
from .serializers import RecipeSerializer

class RecipeListCreateView(generics.ListCreateAPIView):
    # queryset = Recipe.objects.filter(is_published=True)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'rating']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'rating', 'title']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'slug'  # Use slug instead of pk for lookups