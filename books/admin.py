from django.contrib import admin
from .models import Category, Book, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'author', 'description')
    list_editable = ('price', 'stock')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'book__title', 'comment')
    readonly_fields = ('created_at',)

