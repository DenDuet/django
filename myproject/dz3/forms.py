from django import forms
from django.conf import settings


class ImageForm(forms.Form):
    image = forms.ImageField()
    
    
class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=50)
    address = forms.CharField(max_length=50)    
    reg_date = forms.DateTimeField()
    
class Goods(forms.Form):
    goods_name = forms.CharField(max_length=50)
    description = forms.CharField() 
    price = forms.DecimalField(max_digits=8, decimal_places=2)
    quantity = forms.DecimalField(max_digits=8, decimal_places=2) 
    add_date = forms.DateTimeField()   
    image = forms.ImageField()    