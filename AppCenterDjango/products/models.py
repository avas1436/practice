from django.db import models


# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to="products/")
    name = models.CharField(max_length=100)
    description = models.TextField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
