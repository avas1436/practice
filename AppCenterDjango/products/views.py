from django.shortcuts import render


# Create your views here.
def product_list(request):
    products = ["Laptop", "Phone", "Tablet"]
    return render(request, "products/list.html", {"products": products})
