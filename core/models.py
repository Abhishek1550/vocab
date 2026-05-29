from django.db import models

# Create your models here.
class Domain(models.Model):
    """Main category like Kitchen, Travel, Medical, Business etc."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subdomains',
        blank=True,
        null=True,
        help_text="For hierarchical categorization (e.g., Kitchen > Appliances)"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Item(models.Model):
    """A vocabulary item (e.g., Spoon, Knife, Refrigerator)"""
    domain = models.ForeignKey(
        Domain, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    
    image = models.ImageField(
        upload_to='items/', 
        blank=True, 
        null=True,
        help_text="Photo of the object/word"
    )
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['domain', 'created_at']

    def __str__(self):
        # Will show primary word once we get translation
        primary_translation = self.translations.filter(is_primary=True).first()
        if primary_translation:
            return primary_translation.word
        return f"Item {self.id}"

class Translation(models.Model):
    """Translation and details in different languages"""
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='translations'
    )
    
    language_code = models.CharField(
        max_length=10, 
        help_text="ISO code like 'en', 'hi', 'fr', 'es'"
    )
    
    word = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    example_sentence = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_primary = models.BooleanField(
        default=False, 
        help_text="Marks the primary translation for display"
    )

    class Meta:
        unique_together = ('item', 'language_code')  # One translation per language per item
        ordering = ['language_code']

    def __str__(self):
        return f"{self.word} ({self.language_code})"