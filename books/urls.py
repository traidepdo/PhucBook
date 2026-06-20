from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/review/', views.add_review, name='add_review'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.user_list, name='user_list'),
    
    # Category CRUD
    path('admin-dashboard/category/create/', views.category_create, name='category_create'),
    path('admin-dashboard/category/<int:pk>/update/', views.category_update, name='category_update'),
    path('admin-dashboard/category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Book CRUD
    path('admin-dashboard/book/create/', views.book_create, name='book_create'),
    path('admin-dashboard/book/<int:pk>/update/', views.book_update, name='book_update'),
    path('admin-dashboard/book/<int:pk>/delete/', views.book_delete, name='book_delete'),
]
