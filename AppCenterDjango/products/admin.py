from django.contrib import admin

from .models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ("name",)
    sorted_fields = (
        "name",
        "sell_price",
        "buy_price",
        "profit",
        "created_at",
        "updated_at",
    )
    list_display = (
        "image",
        "name",
        "sell_price",
        "buy_price",
        "profit",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
