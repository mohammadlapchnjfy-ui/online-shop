from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', user_register_view, name ='signup'),
    path('login/', user_login_view, name = 'login'),
    path('logout/', user_logout_view, name = 'logout'),
    path('custmer_panel/', customer_panel_view, name = 'customer_panel'),
    path('seller_panel/', seller_panel_view, name= 'seller_panel'),
]
