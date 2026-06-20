from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('shipping', 'Đang giao'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Người dùng")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng tiền")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    shipping_name = models.CharField(max_length=255, verbose_name="Người nhận")
    shipping_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    shipping_phone = models.CharField(max_length=20, verbose_name="Số điện thoại nhận hàng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt hàng")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Đơn hàng")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='order_items', verbose_name="Sách")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá tại thời điểm mua")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.quantity} x {self.book.title if self.book else 'Sách đã xóa'} (Đơn #{self.order.id})"

    @property
    def subtotal(self):
        return self.price * self.quantity
