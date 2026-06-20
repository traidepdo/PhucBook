import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.auth.models import User
from books.models import Category, Book

def seed_data():
    print("Bắt đầu seeding dữ liệu...")

    # 1. Tạo Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@bookstore.vn', 'admin123', first_name='Quản trị', last_name='Nguyễn')
        print("- Đã tạo Admin: username='admin', password='admin123'")
    else:
        print("- Admin 'admin' đã tồn tại.")

    # 2. Tạo Khách hàng thường
    if not User.objects.filter(username='khachhang').exists():
        User.objects.create_user('khachhang', 'khachhang@gmail.com', 'user123', first_name='Khánh', last_name='Trần')
        print("- Đã tạo Khách hàng: username='khachhang', password='user123'")
    else:
        print("- Khách hàng 'khachhang' đã tồn tại.")

    # 3. Tạo Danh mục
    cats_data = [
        {"name": "Sách Văn học", "description": "Tiểu thuyết, truyện ngắn, tác phẩm văn học nổi tiếng trong và ngoài nước."},
        {"name": "Sách Khoa học", "description": "Tài liệu nghiên cứu, khám phá vũ trụ, tự nhiên, công nghệ thông tin."},
        {"name": "Sách Kỹ năng sống", "description": "Phát triển bản thân, tư duy tài chính, giao tiếp ứng xử."},
        {"name": "Sách Thiếu nhi", "description": "Truyện tranh, cổ tích, sách giáo dục cho trẻ nhỏ."}
    ]

    categories = {}
    for cat_info in cats_data:
        cat, created = Category.objects.get_or_create(name=cat_info["name"], defaults={"description": cat_info["description"]})
        categories[cat.name] = cat
        if created:
            print(f"- Đã tạo danh mục: {cat.name}")

    # 4. Tạo Sách mẫu
    books_data = [
        {
            "title": "Số Đỏ",
            "author": "Vũ Trọng Phụng",
            "price": 65000,
            "stock": 25,
            "description": "Tác phẩm trào phúng kinh điển tái hiện xã hội Việt Nam thời kỳ giao thời.",
            "category": categories["Sách Văn học"]
        },
        {
            "title": "Lược Sử Thời Gian",
            "author": "Stephen Hawking",
            "price": 125000,
            "stock": 10,
            "description": "Cuốn sách khoa học phổ thông nổi tiếng nhất giải thích về nguồn gốc vũ trụ.",
            "category": categories["Sách Khoa học"]
        },
        {
            "title": "Đắc Nhân Tâm",
            "author": "Dale Carnegie",
            "price": 86000,
            "stock": 50,
            "description": "Cuốn sách nghệ thuật ứng xử đầu tiên và hay nhất mọi thời đại giúp thay đổi cuộc đời hàng triệu người.",
            "category": categories["Sách Kỹ năng sống"]
        },
        {
            "title": "Dế Mèn Phiêu Lưu Ký",
            "author": "Tô Hoài",
            "price": 45000,
            "stock": 30,
            "description": "Câu chuyện phiêu lưu đầy thú vị của chú Dế Mèn dũng cảm và các bạn nhỏ.",
            "category": categories["Sách Thiếu nhi"]
        }
    ]

    for book_info in books_data:
        book, created = Book.objects.get_or_create(
            title=book_info["title"],
            defaults={
                "author": book_info["author"],
                "price": book_info["price"],
                "stock": book_info["stock"],
                "description": book_info["description"],
                "category": book_info["category"]
            }
        )
        if created:
            print(f"- Đã thêm sách mẫu: {book.title}")

    print("Seeding hoàn tất thành công!")

if __name__ == '__main__':
    seed_data()
