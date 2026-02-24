from django.shortcuts import render

from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, "pages/category.html", {"products": products})
