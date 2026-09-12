from django.db import models

from accounts.models import *


class Store(models.Model):
    name = models.CharField(max_length=15, verbose_name='اسم فروشگاه', null=False, blank= False)
    owner = models.ForeignKey(Seller,on_delete= models.CASCADE,related_name= 'stores')
    description = models.CharField(max_length=100, null=True, blank= True, verbose_name='شرح فروشگاه')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='موجودی حساب فروشگاه')

class Product(models.Model):
    name = models.CharField(max_length= 15, verbose_name= 'اسم محصول', null=False, blank=False )
    stock = models.PositiveIntegerField(verbose_name= 'موجودی', default= 0)
    description = models.CharField(max_length=100, null=True, blank= True, verbose_name='شرح محصول')
    image = models.ImageField(upload_to='product-avatar', null=False, blank= False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='قیمت', null=True)