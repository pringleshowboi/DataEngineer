from django.db import models

# Create your models here.
class Corporation(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'
    
class Store(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField()
