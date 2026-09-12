from django.db.models.signals import post_save
from accounts.models import Customer
from .models import Cart

from django.dispatch import receiver

@receiver(post_save, sender=Customer)
def manage_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer = instance)