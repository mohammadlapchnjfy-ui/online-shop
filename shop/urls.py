from django.urls import path
from .views import *

urlpatterns = [
    path('create_store/', create_store_view, name = 'create_store'),
    path('store_detail/<int:pk>/', store_detail_view, name = 'store_detail'),
    path('add_product/<int:pk>/', add_product_view, name = 'add_product'),
    
]
