from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='products')
    description = models.TextField(max_length=2000)
    quantity =  models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def total_price(self):
        price = 0
        for product in self.products.all():
            price += product.price
        return price


    def __str__(self):
        return self.user.username

