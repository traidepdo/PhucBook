from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('books:index')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"Đăng ký tài khoản '{user.username}' thành công! Bạn có thể đăng nhập ngay.")
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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Chào mừng quay trở lại, {user.username}!")
                # Redirect to next if present
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('books:index')
        messages.error(request, "Tên đăng nhập hoặc mật khẩu không chính xác.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Bạn đã đăng xuất tài khoản thành công.")
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
