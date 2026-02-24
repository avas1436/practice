from django.shortcuts import render
from products.models import Product


# Create your views here.
def core_view(request):
    featured_products = Product.objects.order_by("-created_at")[:8]  # آخرین 8 محصول
    return render(request, "pages/home.html", {"featured_products": featured_products})
