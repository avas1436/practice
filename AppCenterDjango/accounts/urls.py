from django.urls import path
from views import account_list

urlpatterns = [
    path("accounts/", account_list, name="account_list"),
]
