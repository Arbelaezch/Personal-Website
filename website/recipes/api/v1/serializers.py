from rest_framework import serializers
from recipes.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    total_time = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 
            'title',
            'slug',
            'description',
            'servings',
            'prep_time',
            'cook_time',
            'total_time',
            'difficulty',
            'ingredients',
            'directions',
            'category',
            'image_url',
            'rating',
            'created_at',
            'updated_at',
            'is_published'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


    def get_total_time(self, obj):
        return obj.get_total_time()
    
    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None