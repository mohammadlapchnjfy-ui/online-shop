from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if form.is_valid() :
            role = form.cleaned_data['role']
            
            if role == 'customer':
            
                
                
                if customer_form.is_valid():
                    with transaction.atomic():
                
                        user = form.save()
                        customer = customer_form.save(commit=False)
                        customer.user = user
                        customer.save() 
                    login(request, user)
                    messages.success(request, f'جناب مشتری{user.first_name}با موفقیت وارد شد')
            
                    return redirect('home')
            elif role == 'seller':
                with transaction.atomic():
                    user = form.save()
                    seller = Seller.objects.create(user = user)
                login(request, user)
                messages.success(request, f'جناب فروشنده{user.first_name}با موفقیت وارد شد')  
            
                return redirect('home')  
        else:    
                messages.error(request, f'ثبت نام موفقیت آمیز نبود ')
    
    else:
        form = UserRegisterForm()
        customer_form = CustomerForm()
    
    return render(request, 'registration/signup.html', {'form' : form, 'customer_form' : customer_form})


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})           

def user_logout_view(request):
    logout(request)
    return redirect(reverse('home'))

def get_user_role(user):
    if hasattr(user, 'customer_profile'):
        return 'customer'
    if hasattr(user, 'seller_profile'):
        return 'seller'
    return None


@login_required
def customer_panel_view(request):
    customer = request.user.customer_profile
    role = get_user_role(request.user)
    if role == 'seller':
        raise PermissionDenied
    
    return render(request, 'customer_panel.html', {'customer' : customer})



@login_required
def seller_panel_view(request):
    
    role = get_user_role(request.user)
    if role != 'seller':
        raise PermissionDenied
    seller = request.user.seller_profile
    stores =seller.stores.all()
    
    return render(request, 'seller_panel.html', {'seller' : seller, 'stores' : stores })

