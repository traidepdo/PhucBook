from django.db import models

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
