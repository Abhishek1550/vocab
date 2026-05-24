from django.contrib import admin

# Register your models here.
from .models import *
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'created_at', 'updated_at')
    list_filter = ('domain',)
    search_fields = ('translations__word',)

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('item', 'language_code', 'word', 'is_primary', 'created_at', 'updated_at')
    list_filter = ('language_code', 'is_primary')
    search_fields = ('word',)

