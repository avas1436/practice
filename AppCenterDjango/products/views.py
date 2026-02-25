from django.shortcuts import render

from .models import Product


def product_list(request):
    products = Product.objects.only(
        "image",
        "name",
        "description",
        "sell_price",
        "profit",
    )
    return render(request, "pages/category.html", {"products": products})
