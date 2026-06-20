from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_name', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('shipping_name', 'shipping_phone', 'user__username')
    inlines = [OrderItemInline]
