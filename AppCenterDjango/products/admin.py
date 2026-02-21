from django.contrib import admin

from .models import product


# Register your models here.
@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ("name",)
    sorted_fields = ("name", "price", "created_at", "updated_at")
    list_display = ("name", "price", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
