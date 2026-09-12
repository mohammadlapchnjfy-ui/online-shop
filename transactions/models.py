from django.db import models
from accounts.models import *
from shop.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product','cart'], name='unique_product_cart')
        ]    
    
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2,verbose_name='مجموع خرید')
    StatusType = models.TextChoices(
        "StatusType",
        "PENDING PAID CANCELLED"
    )
    status = models.CharField(
        max_length=10,
        choices=StatusType,
        default=StatusType.PENDING
    )
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitems')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='قیمت')
    

    

