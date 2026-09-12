from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from accounts.views import get_user_role
from django.core.exceptions import PermissionDenied



@login_required
def create_store_view(request):
    if request.method == 'POST':
        form = StoreCreateForm(request.POST)
        if form.is_valid():
            role = get_user_role(request.user)
            if role == 'seller':
                owner = request.user.seller_profile
                store = form.save(commit=False)
                store.owner = owner
                store.save()
                return redirect('seller_panel')
            if role != 'seller':
                raise PermissionDenied
        
    else:
        form = StoreCreateForm()
    return render(request, 'create_store.html', {'form' : form})




def store_detail_view(request, pk):
    store = get_object_or_404(Store, pk = pk)
    products = store.products.all()
    return render(request, 'store_detail.html', {'store' : store, 'products' : products})



@login_required
def add_product_view(request, pk):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        store = get_object_or_404(Store, pk=pk)
        role = get_user_role(request.user)

        if role == 'seller':
            owner = store.owner
            user = request.user.seller_profile

            if user == owner:
                if form.is_valid():
                    product = form.save(commit=False)
                    product.store = store
                    product.save()
                    

                    return redirect('store_detail', pk=store.pk)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    else:
        form = ProductAddForm()

    return render(request, 'add_product.html', {'form': form})

  

