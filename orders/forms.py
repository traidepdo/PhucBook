from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_name', 'shipping_phone', 'shipping_address']
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập đầy đủ họ tên người nhận'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại nhận hàng'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ giao hàng chi tiết', 'rows': 3}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
