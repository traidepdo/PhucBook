from django import forms
from .models import Category, Book

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên danh mục'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập mô tả danh mục (tùy chọn)', 'rows': 3}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'stock', 'description', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tiêu đề sách'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên tác giả'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập giá bán', 'step': '1000'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số lượng tồn kho'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập mô tả sách', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
