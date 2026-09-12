def user_role(request):
    role = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'customer_profile'):
            role = 'customer'
        if hasattr(request.user, 'seller_profile'):
            role = 'seller'
            
    return {'user_role' : role}        