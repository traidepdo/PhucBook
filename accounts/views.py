from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm, EmailAuthenticationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('books:index')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"Đăng ký tài khoản thành công! Chào mừng bạn đến với BookStore.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Đăng ký không thành công. Vui lòng kiểm tra lại thông tin.")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('books:index')
        
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data.get('login_input')
            password = form.cleaned_data.get('password')

            # Thử đăng nhập bằng username trực tiếp
            user = authenticate(request, username=login_input, password=password)
            
            # Nếu không được, thử tìm username qua email
            if user is None:
                try:
                    db_user = User.objects.get(email__iexact=login_input)
                    user = authenticate(request, username=db_user.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Chào mừng quay trở lại, {user.first_name or user.username}! 👋")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('books:index')
            else:
                messages.error(request, "Email/tên đăng nhập hoặc mật khẩu không chính xác.")
        else:
            messages.error(request, "Vui lòng điền đầy đủ thông tin đăng nhập.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Bạn đã đăng xuất thành công. Hẹn gặp lại!")
    return redirect('books:index')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin cá nhân thành công!")
            return redirect('accounts:profile')
        messages.error(request, "Có lỗi xảy ra. Vui lòng sửa các lỗi bên dưới.")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
