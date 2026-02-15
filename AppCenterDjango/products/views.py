from django.shortcuts import render


# Create your views here.
def product_list(request):
    # products = ["Laptop", "Phone", "Tablet"]
    products = [
        {"name": "Laptop", "description": "First app description", "price": 29},
        {"name": "Phone", "description": "Second app description", "price": 49},
        {"name": "Tablet", "description": "Third app description", "price": 19},
    ]
    return render(request, "products.html", {"products": products})
