from django.shortcuts import render


# Create your views here.
def order_list(request):
    orders = ["Order 1", "Order 2", "Order 3"]
    return render(request, "orders/list.html", {"orders": orders})
