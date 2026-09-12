from django import forms



class IncreaseBalanceForm(forms.Form):
    amount = forms.DecimalField(max_digits=12,decimal_places=2,label= 'مقدار')
    
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value= 1, label= 'quantity')