from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomerInline(admin.StackedInline):
    model = Customer
    extra = 0
    
class SellerInline(admin.StackedInline):
    model = Seller
    extra = 0
    
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [CustomerInline, SellerInline]    
    