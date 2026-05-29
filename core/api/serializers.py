from rest_framework import serializers
from ..models import Domain, Item, Translation

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'language_code', 'word', 'description', 'example_sentence', 'is_primary']


class ItemSerializer(serializers.ModelSerializer):
    translations = TranslationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'image', 'created_at', 'updated_at', 'translations']


class DomainSerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Domain
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'items_count']