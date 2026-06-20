from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if book is in stock
    if book.stock <= 0:
        messages.error(request, f"Xin lỗi, sách '{book.title}' đã hết hàng.")
        return redirect('books:book_detail', pk=book_id)
        
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if not item_created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > book.stock:
            messages.warning(request, f"Chỉ có thể thêm tối đa {book.stock} cuốn sách '{book.title}'.")
            cart_item.quantity = book.stock
        else:
            cart_item.quantity = new_quantity
            messages.success(request, f"Đã thêm {quantity} cuốn '{book.title}' vào giỏ hàng.")
    else:
        if quantity > book.stock:
            messages.warning(request, f"Chỉ có thể thêm tối đa {book.stock} cuốn sách '{book.title}'.")
            cart_item.quantity = book.stock
        else:
            cart_item.quantity = quantity
            messages.success(request, f"Đã thêm '{book.title}' vào giỏ hàng.")
            
    cart_item.save()
    return redirect('cart:cart_detail')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity <= 0:
                cart_item.delete()
                messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
            elif quantity > cart_item.book.stock:
                messages.warning(request, f"Số lượng yêu cầu vượt quá tồn kho. Đã cập nhật thành tối đa ({cart_item.book.stock}).")
                cart_item.quantity = cart_item.book.stock
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cập nhật số lượng thành công.")
        except (ValueError, TypeError):
            messages.error(request, "Số lượng không hợp lệ.")
            
    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    book_title = cart_item.book.title
    cart_item.delete()
    messages.success(request, f"Đã xóa sách '{book_title}' khỏi giỏ hàng.")
    return redirect('cart:cart_detail')
