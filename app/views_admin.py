from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Order, CartItem
from django.db.models import Sum, Count

@staff_member_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
    recent_orders = Order.objects.order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_stock': total_stock,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/dashboard.html', context)