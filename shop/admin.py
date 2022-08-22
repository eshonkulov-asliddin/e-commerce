from django.contrib import admin
from .models import Category, Product

from parler.admin import TranslatableAdmin

# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    #instead of prepopulated_field, because django-parler do not allow to use it
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    #instead of prepopulated_field, because django-parler do not allow to use it
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}