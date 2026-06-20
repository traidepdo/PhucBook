from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả danh mục")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tiêu đề sách")
    author = models.CharField(max_length=255, verbose_name="Tác giả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá bán")
    stock = models.PositiveIntegerField(default=0, verbose_name="Số lượng tồn kho")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả sách")
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name="Ảnh bìa")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name="Danh mục")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày nhập")

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Sách"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Sách")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Người dùng")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Đánh giá (sao)"
    )
    comment = models.TextField(verbose_name="Nhận xét")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đánh giá")

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ['-created_at']
        # Mỗi người chỉ được đánh giá 1 lần cho mỗi sách
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} đánh giá '{self.book.title}' – {self.rating} sao"
