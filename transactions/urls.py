from django.urls import path
from .views import *

urlpatterns = [
    path('payment/', increace_balance_view, name = 'payment'),
    path('add_to_cart/<int:pk>/', add_to_cart_view, name = 'add_to_cart'),
    path('cart/', view_cart, name = 'cart'),
    path('check_out/', check_out_view, name = 'checkout'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('order_history/', order_history_view, name='order_history'),
]
