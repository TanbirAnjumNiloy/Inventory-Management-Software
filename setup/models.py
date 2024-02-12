from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .models import *
 
class Supplier(models.Model):
    sname = models.CharField(max_length=100)
    saddress = models.CharField(max_length=100)
    smobile = models.CharField(max_length=100)
    sbalance = models.FloatField()

    def __str__(self):
        return self.sname

class Brand(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Market(models.Model):
    area = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    number = models.IntegerField()

    def __str__(self):
        return self.address

class Dsr(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    



class Bank(models.Model):
    BANK_TYPE_CHOICES = (
        ('Deposit', 'Deposit A/c'),
        ('CC', 'CC A/c'),
    )
    bank_name = models.CharField(max_length=50)
    account_no = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    account_type = models.CharField(max_length=10, choices=BANK_TYPE_CHOICES, default='Deposit')

    def __str__(self):
        return self.bank_name

class Product(models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    commission = models.DecimalField(max_digits=5, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0) 
    

    def __str__(self):
        return self.name

    

class Doprice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.price}"
    

class Sellprice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    added_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.product.name} - {self.price}"
    


class Salesmanager(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Discountsetup(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

    
class Collectionsetup(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class GramSetup(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gram_setups')
    grams = models.FloatField()
    current_grams = models.FloatField() 
    




    