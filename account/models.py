from django.db import models
from datetime import date
from django.db.models import Max

from .models import *
from setup.models import *

# Create your models here.

class Lifting(models.Model):
    date = models.DateField()
    invoicing = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    Doprice = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.date}'
    def item_type(self):
        return "Lifting"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sell_price = models.ForeignKey(Sellprice, on_delete=models.CASCADE)
    dsr = models.ForeignKey(Dsr, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    total_commission = models.FloatField()
    date = models.DateField(null=True)
    mem_number = models.PositiveIntegerField()


    def save(self, *args, **kwargs):
        if not self.mem_number:
            max_mem_number = Sales.objects.all().aggregate(Max('mem_number'))['mem_number__max']
            self.mem_number = max_mem_number + 1 if max_mem_number else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} - {self.product.size} - {self.date} - {self.mem_number}'
    
class Damage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Purchase_Price = models.ForeignKey(Doprice, on_delete=models.CASCADE)
    sales_Price = models.ForeignKey(Sellprice, on_delete=models.CASCADE, unique=False)  # Set unique=False or remove the unique attribute
    date = models.DateField(null=True)
    mem_number = models.PositiveIntegerField(unique=False)
    qty = models.PositiveIntegerField(default=0)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.mem_number:
            max_mem_number = Damage.objects.all().aggregate(Max('mem_number'))['mem_number__max']
            self.mem_number = max_mem_number + 1 if max_mem_number else 1

        if self.qty and self.sales_Price and self.Purchase_Price:
            self.sales_amount = self.qty * self.sales_Price.price
            self.purchase_amount = self.qty * self.Purchase_Price.price

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} - {self.date} - {self.mem_number}'
    

class BankTransaction(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank.bank_name} - {self.bank.branch} - {self.bank.account_no} - {self.amount}"
    

    from django.db import models
from .models import Supplier, Bank

class SupplierPayment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"Payment of {self.amount} to {self.supplier.sname} on {self.date} on {self.bank.account_no}"
    def item_type(self):
        return "SupplierPayment"
    

class Acdiccount(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sr = models.ForeignKey(Salesmanager, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discountsetup, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Add this field

    def __str__(self):
        return f"  {self.supplier.sname} , {self.discount}, {self.sr} , {self.date}, {self.amount} "
    


class Dailycost(models.Model):
    dsr = models.ForeignKey(Dsr, on_delete=models.CASCADE)
    date = models.DateField()
    carcost = models.DecimalField(max_digits=10, decimal_places=2) 
    dsrbill = models.DecimalField(max_digits=10, decimal_places=2) 
    toll = models.DecimalField(max_digits=10, decimal_places=2) 
    othercost = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"  {self.dsr} , {self.carcost}, {self.dsrbill} , {self.toll}, {self.othercost},  {self.date} "


class CollectionTransaction(models.Model):
    collection_man = models.ForeignKey(Collectionsetup, on_delete=models.CASCADE)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Assets(models.Model):
    date = models.DateField()
    shop_due = models.DecimalField(max_digits=10, decimal_places=2)
    rashed_due = models.DecimalField(max_digits=10, decimal_places=2)
    bazar_due = models.DecimalField(max_digits=10, decimal_places=2)
    tso = models.DecimalField(max_digits=10, decimal_places=2)
    milon = models.DecimalField(max_digits=10, decimal_places=2)
    bank_check = models.DecimalField(max_digits=10, decimal_places=2)
    mehdi_sr = models.DecimalField(max_digits=10, decimal_places=2)
    card = models.DecimalField(max_digits=10, decimal_places=2)
    damage = models.DecimalField(max_digits=10, decimal_places=2)
    naitrogen_damage = models.DecimalField(max_digits=10, decimal_places=2)
    robiul_sr = models.DecimalField(max_digits=10, decimal_places=2)
    pubali_bank = models.DecimalField(max_digits=10, decimal_places=2)
    robiul_dsr = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    other = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Assets record for {self.date}"









    
