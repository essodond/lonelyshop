from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from app.admin import ProductAdmin
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User
from django.http import HttpResponse

# Product listing

def product_list(request):
    products = Product.objects.all()
    return render(request, 'Produit/produit.html', {'produits': products})

# Product detail

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'Produit/detail.html', {'produit': product})

# Add to cart

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        quantity = int(request.POST.get('quantite', 1))
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('panier')
    return HttpResponse(status=400)

# View cart

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'Panier/panier.html', {'items': items, 'total': total})

# Remove from cart

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('panier')

# Place order

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    if not items:
        return redirect('panier')
    order = Order.objects.create(user=request.user, total_price=0)
    total = 0
    for item in items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        total += item.product.price * item.quantity
        # Update stock
        item.product.stock -= item.quantity
        item.product.save()
    order.total_price = total
    order.save()
    # Clear cart
    items.delete()
    return redirect('commande')

# View orders

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Commande/commande.html', {'orders': orders})

# User login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'conn/connect.html', {'error': 'Invalid credentials'})
    return render(request, 'conn/connect.html')

# User logout

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

# User registration

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            return render(request, 'conn/inscript.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('index')
    return render(request, 'conn/inscript.html')

# Home page

def index(request):
    # Get first 6 products with their image, name and price
    produits = Product.objects.all()  # Récupère tous les produits
    return render(request, 'index.html', {'produits': produits})


# Update quantity

@login_required
def update_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "increase":
            item.quantity += 1
        elif action == "decrease":
            item.quantity = max(1, item.quantity - 1)  # minimum 1

        item.save()

    return redirect('panier')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def cart_quantity_api(request):
    # Suppose que tu as un modèle Cart lié à l'utilisateur
    cart = Cart.objects.filter(user=request.user).first()
    quantity = 0
    if cart:
        quantity = sum(item.quantity for item in cart.items.all())
    return JsonResponse({'quantity': quantity})
