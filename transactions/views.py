from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from accounts.views import get_user_role
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import *
from shop.models import Product
from django.db import transaction



@login_required
def increace_balance_view(request):
    if request.method == 'POST':
        form = IncreaseBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            role = get_user_role(request.user)
            if role == 'customer':
                customer = request.user.customer_profile
                customer.balance += amount
                
                customer.save()
                
                return redirect('customer_panel')
            if role != 'customer':
                raise PermissionDenied
                
    else:
            form = IncreaseBalanceForm()
        
    return render(request, 'payment.html', {'form': form})  



@login_required
def add_to_cart_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        role = get_user_role(request.user)
        
        if form.is_valid():
            if role == 'customer':
                quantity = form.cleaned_data['quantity']
                
                stock = product.stock
                customer = request.user.customer_profile
                if quantity <= stock:
                    cart = customer.cart
                    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product, defaults={'quantity' : quantity})
                    if not created :
                         
                        new_quantity = cart_item.quantity + quantity
                        if new_quantity <= stock:
                            cart_item.quantity+=quantity
                            cart_item.save()
                            return redirect('cart')
                        else:
                            form.add_error('quantity', 'Not Enough Stock')
                    if created:
                        return redirect('cart')

                else:
                    form.add_error('quantity', 'Not Enough Stock ')
            else:
                raise PermissionDenied
    else:
        form = AddToCartForm()
    return render(request, 'add_to_cart.html', {'form' : form, 'product' : product})

@login_required
def view_cart(request):
    role = get_user_role(request.user)
    if role != 'customer':
        raise PermissionDenied
    customer = request.user.customer_profile
    cart = customer.cart
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity
                for item in cart_items)
    return render(request, 'cart.html', {'cart_items' : cart_items, 'total' : total})




            
            
            
@login_required
def check_out_view(request):
    role = get_user_role(request.user)

    if role != 'customer':
        raise PermissionDenied

    with transaction.atomic():

        customer = Customer.objects.select_for_update().get(
            id=request.user.customer_profile.id
        )

        cart = customer.cart
        cart_items = list(cart.items.select_related('product').all())

        product_ids = [item.product_id for item in cart_items]

        products = Product.objects.select_for_update().filter(
            id__in=product_ids
        ).order_by('id')

        products = {
            product.id: product
            for product in products
        }

        total = 0

        for item in cart_items:
            product = products[item.product_id]

            if product.stock < item.quantity:
                return redirect('cart')

            total += product.price * item.quantity

        if customer.balance < total:
            return redirect('cart')

        store_ids = {
            product.store_id
            for product in products.values()
        }

        stores = Store.objects.select_for_update().filter(
            id__in=store_ids
        ).order_by('id')

        stores = {
            store.id: store
            for store in stores
        }

        order = Order.objects.create(
            customer=customer,
            total_amount=total
        )

        for item in cart_items:

            product = products[item.product_id]
            store = stores[product.store_id]

            OrderItem.objects.create(
                product=product,
                quantity=item.quantity,
                price=product.price,
                order=order
            )

            product.stock -= item.quantity
            product.save(update_fields=['stock'])

            total_balance = product.price * item.quantity

            store.balance += total_balance
            store.save(update_fields=['balance'])

        customer.balance -= total
        customer.save(update_fields=['balance'])

        order.status = Order.StatusType.PAID
        order.save(update_fields=['status'])

        cart.items.all().delete()

        return redirect('cart')
    
    
    
@login_required
def remove_from_cart(request, pk):
    role = get_user_role(request.user)
    if role != 'customer':
        raise PermissionDenied
    customer = request.user.customer_profile
    cart = customer.cart
    cart_item = get_object_or_404(cart.items, pk = pk)
    cart_item.delete()
    return redirect('cart')
   
   

@login_required
def order_history_view(request):
    role = get_user_role(request.user)
    if role != 'customer':
        raise PermissionDenied
    customer = request.user.customer_profile
    orders = customer.orders.all().order_by('-created_at')
    return render(request, 'order_history.html', {'order_history' : orders})
                    

            
                          
            


