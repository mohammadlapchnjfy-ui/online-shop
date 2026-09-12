from django import forms
from .models import Store, Product



class StoreCreateForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description']
        

class ProductAddForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'stock', 'description', 'image', 'price']  
        
        