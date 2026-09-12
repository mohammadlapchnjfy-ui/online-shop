from django.shortcuts import render
from shop.models import Product, Store

def home_view(request):
    products = Product.objects.order_by('-created_at')[:20]
    return render(request, 'home.html', {'products' : products})


def stores_view(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores' : stores})
