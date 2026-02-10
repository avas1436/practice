from django.shortcuts import render

# Create your views here.


def account_list(request):
    accounts = ["avAs", "sama", "rez"]
    return render(request, "accounts/list.html", {"accounts": accounts})
