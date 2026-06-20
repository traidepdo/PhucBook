from django import forms
from django.contrib.auth.models import User

class EmailAuthenticationForm(forms.Form):
    """Form đăng nhập hỗ trợ cả email lẫn username"""
    login_input = forms.CharField(
        label="Email hoặc tên đăng nhập",
        widget=forms.TextInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Email hoặc tên đăng nhập',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Mật khẩu',
            'autocomplete': 'current-password',
        })
    )

class RegistrationForm(forms.ModelForm):
    """Form đăng ký tài khoản mới"""
    first_name = forms.CharField(
        label="Tên",
        widget=forms.TextInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Tên của bạn',
        }),
        max_length=30
    )
    last_name = forms.CharField(
        label="Họ",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Họ của bạn (tuỳ chọn)',
        }),
        max_length=150
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Tối thiểu 6 ký tự',
            'autocomplete': 'new-password',
        }),
        min_length=6
    )
    confirm_password = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Nhập lại mật khẩu',
            'autocomplete': 'new-password',
        }),
        min_length=6
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Tên đăng nhập (chữ, số, dấu _)',
                'autocomplete': 'username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'auth-input',
                'placeholder': 'example@email.com',
                'autocomplete': 'email',
            }),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Địa chỉ Email',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email này đã được đăng ký. Hãy dùng email khác.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Tên đăng nhập này đã tồn tại.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Mật khẩu xác nhận không khớp.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ email'}),
        }
        labels = {
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email',
        }
