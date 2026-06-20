from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderCreateForm, OrderStatusForm
from cart.models import Cart
from books.views import is_admin

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if cart.items.count() == 0:
        messages.error(request, "Giỏ hàng của bạn đang trống. Vui lòng thêm sản phẩm trước khi thanh toán.")
        return redirect('cart:cart_detail')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Use transaction to ensure order and stock update are atomic
            try:
                with transaction.atomic():
                    # Double-check stock before placing order
                    for item in cart.items.all():
                        if item.quantity > item.book.stock:
                            raise ValueError(f"Sách '{item.book.title}' chỉ còn {item.book.stock} cuốn trong kho. Vui lòng cập nhật giỏ hàng.")
                            
                    # Create Order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = cart.total_price
                    order.save()
                    
                    # Create OrderItems and deduct stock
                    for item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            book=item.book,
                            quantity=item.quantity,
                            price=item.book.price
                        )
                        # Deduct book stock
                        book = item.book
                        book.stock -= item.quantity
                        book.save()
                        
                    # Clear Cart
                    cart.items.all().delete()
                    
                    messages.success(request, f"Đặt hàng thành công! Đơn hàng của bạn là #{order.id}.")
                    return redirect('orders:order_history')
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "Đã xảy ra lỗi trong quá trình xử lý đơn hàng. Vui lòng thử lại.")
    else:
        # Pre-fill name if user has it
        initial_data = {}
        if request.user.first_name or request.user.last_name:
            initial_data['shipping_name'] = f"{request.user.last_name} {request.user.first_name}".strip()
        form = OrderCreateForm(initial=initial_data)
        
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@user_passes_test(is_admin, login_url='accounts:login')
def admin_orders(request):
    orders = Order.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/admin_orders.html', {
        'orders': orders,
        'status_filter': status_filter
    })

@user_passes_test(is_admin, login_url='accounts:login')
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cập nhật trạng thái đơn hàng #{order.id} thành công.")
            return redirect('orders:admin_order_detail', pk=order.id)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'orders/admin_order_detail.html', {
        'order': order,
        'form': form
    })
