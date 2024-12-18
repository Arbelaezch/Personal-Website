from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Recipe(models.Model):
    CATEGORIES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('appetizer', 'Appetizer'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
    )

    DIFFICULTY = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )
    
    # Required fields
    title = models.CharField(max_length=100)
    ingredients = RichTextField(help_text="Enter each ingredient on a new line in format: '2 cups flour' or '1 tablespoon sugar'")
    directions = RichTextField(help_text="Enter each step on a new line. They will be automatically numbered.")

    # Optional fields
    slug = models.SlugField(unique=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=3, blank=True, null=True)
    description = RichTextField(blank=True, help_text="Brief introduction to the recipe")
    
    servings = models.PositiveIntegerField(blank=True, null=True, help_text="Number of servings this recipe makes")
    prep_time = models.PositiveIntegerField(blank=True, null=True, help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(blank=True, null=True, help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='medium', blank=True)
    
    notes = RichTextField(blank=True, help_text="Additional tips, variations, or storage instructions")
    nutrition_info = models.TextField(blank=True, help_text="Nutritional information per serving")
    category = models.CharField(max_length=100, choices=CATEGORIES, blank=True)
    image = models.ImageField(
        upload_to='recipe_images',
        blank=True,
        null=True,
        help_text="Main recipe image"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_total_time(self):
        """Returns total time in minutes (prep + cooking)"""
        if self.prep_time and self.cook_time:
            return self.prep_time + self.cook_time
        return None
    
    def save(self, *args, **kwargs):
        if not self.slug:  # If no slug exists, create one from the title
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)