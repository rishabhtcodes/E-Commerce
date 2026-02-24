from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.services import CartManager
from accounts.email_service import EmailService

@login_required
def checkout(request):
    cart_manager = CartManager(request.user)
    if not cart_manager.cart or cart_manager.cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart:cart_detail')
        
    if request.method == 'POST':
        from .services import CheckoutService
        order, message = CheckoutService.process_checkout(request.user)
        
        if order:
            # Send order confirmation email
            EmailService.send_order_confirmation(request.user, order)
            messages.success(request, f"{message} Check your email for confirmation.")
            return redirect('orders:success', order_id=order.id)
        else:
            messages.error(request, message)
            return redirect('cart:cart_detail')
            
    return render(request, 'orders/checkout.html', {
        'cart': cart_manager.cart,
        'total_price': cart_manager.calculate_total()
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
def update_order_status(request, order_id, status):
    if request.user.role != 'seller':
        messages.error(request, "Only sellers can perform this action.")
        return redirect('product_list')
        
    order = get_object_or_404(Order, id=order_id)
    # Check if the seller has any product in this order
    if not order.items.filter(product__seller=request.user).exists():
        messages.error(request, "You cannot modify this order.")
        return redirect('seller_dashboard')
        
    if request.method == 'POST' and status in ['Shipped', 'Cancelled']:
        order.status = status
        order.save()
        verb = "allowed (shipped)" if status == "Shipped" else "cancelled"
        messages.success(request, f"Order #{order.id} has been {verb}.")
        
    return redirect('seller_dashboard')
