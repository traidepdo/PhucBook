from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Book, Category
from .forms import BookForm, CategoryForm
from orders.models import Order

# Helper to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# Home page / Index view
def index(request):
    featured_books = Book.objects.order_by('-created_at')[:4]
    latest_books = Book.objects.order_by('-created_at')[4:8]
    return render(request, 'books/index.html', {
        'featured_books': featured_books,
        'latest_books': latest_books,
    })

# Book list with search, filter, and pagination
def book_list(request):
    books_query = Book.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    if query:
        books_query = books_query.filter(title__icontains=query) | books_query.filter(author__icontains=query)
        
    if category_id:
        books_query = books_query.filter(category_id=category_id)

    paginator = Paginator(books_query, 6) # 6 sách mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)

    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'query': query,
        'selected_category': selected_category,
    })

# Book detail view
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    related_books = Book.objects.filter(category=book.category).exclude(pk=pk)[:4]
    return render(request, 'books/book_detail.html', {
        'book': book,
        'related_books': related_books,
    })

# Admin Dashboard
@user_passes_test(is_admin, login_url='accounts:login')
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    categories = Category.objects.all()
    books = Book.objects.all().order_by('-created_at')
    
    return render(request, 'books/admin_dashboard.html', {
        'total_books': total_books,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'categories': categories,
        'books': books,
    })

# Category CRUD
@user_passes_test(is_admin, login_url='accounts:login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Đã thêm danh mục '{category.name}' thành công.")
            return redirect('books:admin_dashboard')
    else:
        form = CategoryForm()
    return render(request, 'books/category_form.html', {'form': form, 'title': 'Thêm danh mục mới'})

@user_passes_test(is_admin, login_url='accounts:login')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật danh mục '{category.name}' thành công.")
            return redirect('books:admin_dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'books/category_form.html', {'form': form, 'title': 'Cập nhật danh mục'})

@user_passes_test(is_admin, login_url='accounts:login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"Đã xóa danh mục '{category_name}' thành công.")
        return redirect('books:admin_dashboard')
    return render(request, 'books/category_confirm_delete.html', {'category': category})

# Book CRUD
@user_passes_test(is_admin, login_url='accounts:login')
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Đã thêm sách '{book.title}' thành công.")
            return redirect('books:admin_dashboard')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Thêm sách mới'})

@user_passes_test(is_admin, login_url='accounts:login')
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật thông tin sách '{book.title}' thành công.")
            return redirect('books:admin_dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Cập nhật sách'})

@user_passes_test(is_admin, login_url='accounts:login')
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f"Đã xóa sách '{book_title}' thành công.")
        return redirect('books:admin_dashboard')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# List Users for Admin
@user_passes_test(is_admin, login_url='accounts:login')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'books/user_list.html', {'users': users})
