from django.conf import settings
from django.db import models
from django.core.management.base import BaseCommand

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)      
    address = models.CharField(max_length=150)
    reg_date = models.DateTimeField(auto_now_add=False)
    
    def __str__(self):
        return f'Username: {self.username}, email: {self.email}, phone: {self.phone}'

class Goods(models.Model):
    goods_name = models.CharField(max_length=50)
    description = models.TextField() 
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2) 
    add_date = models.DateTimeField(auto_now_add=False)   
    image = models.ImageField(upload_to =settings.MEDIA_ROOT)
    def __str__(self):
        return f'Product: {self.goods_name}, price: {self.price}, quantity: {self.quantity}'    

class Orders(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Goods)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)    
    date_ordered = models.DateTimeField(auto_now_add=False)
    def __str__(self):
       return f'Order of user: {self.customer.username}, total: {self.total_price}'    
   
   
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(default=999999.99, max_digits=8,decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(default=5.0, max_digits=3, decimal_places=2)
    
    def __str__(self):
        return self.name 
