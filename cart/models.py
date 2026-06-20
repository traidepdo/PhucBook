from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Người dùng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Giỏ hàng"
        verbose_name_plural = "Giỏ hàng"

    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"

    @property
    def total_price(self):
        # Tính tổng giá trị giỏ hàng
        return sum(item.subtotal for item in self.items.all())

    @property
    def items_count(self):
        # Tính tổng số lượng sản phẩm trong giỏ hàng
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Giỏ hàng")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Sách")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")

    class Meta:
        verbose_name = "Sản phẩm giỏ hàng"
        verbose_name_plural = "Sản phẩm giỏ hàng"

    def __str__(self):
        return f"{self.quantity} x {self.book.title} (Giỏ của {self.cart.user.username})"

    @property
    def subtotal(self):
        # Thành tiền của từng item
        return self.book.price * self.quantity
