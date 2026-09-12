from django.contrib import admin
from .models import *

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
    search_fields = ('customer__phone',)
    inlines = [CartItemInline]    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'customer', 'total_amount', 'status') 
    search_fields = ('customer__phone',)
    list_editable = ('status',)
    inlines = [OrderItemInline]
