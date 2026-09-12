from django.db import models

from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name= 'seller_profile')
    
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'customer_profile')
    phone = models.CharField(max_length=11, unique=True, verbose_name= 'شماره تلفن', null=False, blank=False)
    balance = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default= 0,
    verbose_name='موجودی',
)  