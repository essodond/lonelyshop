from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from app.admin import ProductAdmin
from .models import Product, Cart, CartItem, Order, OrderItem, Payment
from django.contrib.auth.models import User
from django.http import HttpResponse

# Product listing

def product_list(request):
    # Get all products with their descriptions and sizes
    products = Product.objects.all()
    return render(request, 'Produit/produit.html', {
        'produits': products,
    })

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
    
    # Vérifier le stock disponible
    for item in items:
        if item.quantity > item.product.stock:
            return render(request, 'Panier/panier.html', {
                'items': items,
                'total': sum(item.product.price * item.quantity for item in items),
                'error': f'Stock insuffisant pour {item.product.name}. Stock disponible: {item.product.stock}'
            })
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            return render(request, 'Panier/panier.html', {
                'items': items,
                'total': sum(item.product.price * item.quantity for item in items),
                'error': 'Veuillez sélectionner une méthode de paiement'
            })

        try:
            order = Order.objects.create(user=request.user, total_price=0)
            total = 0
            for item in items:
                if item.quantity > item.product.stock:
                    order.delete()
                    return render(request, 'Panier/panier.html', {
                        'items': items,
                        'total': sum(item.product.price * item.quantity for item in items),
                        'error': f'Stock insuffisant pour {item.product.name}. Stock disponible: {item.product.stock}'
                    })
                
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                total += item.product.price * item.quantity
                item.product.stock -= item.quantity
                item.product.save()
            
            order.total_price = total
            order.save()

            # Créer le paiement
            payment = Payment.objects.create(
                order=order,
                method=payment_method,
                amount=total
            )

            # Si paiement mobile (Flooz ou Mixx)
            if payment_method in ['FLOOZ', 'MIXX']:
                phone_number = request.POST.get('phone_number')
                if not phone_number:
                    order.delete()
                    return render(request, 'Panier/panier.html', {
                        'items': items,
                        'total': total,
                        'error': 'Numéro de téléphone requis pour le paiement mobile'
                    })
                payment.phone_number = phone_number
                payment.save()

            # Si paiement par carte
            elif payment_method == 'CARD':
                card_number = request.POST.get('card_number')
                card_expiry = request.POST.get('card_expiry')
                card_cvv = request.POST.get('card_cvv')
                
                if not all([card_number, card_expiry, card_cvv]):
                    order.delete()
                    return render(request, 'Panier/panier.html', {
                        'items': items,
                        'total': total,
                        'error': 'Informations de carte bancaire incomplètes'
                    })
                    
                payment.card_number = card_number
                payment.card_expiry = card_expiry
                payment.card_cvv = card_cvv
                payment.save()

            # Clear cart
            items.delete()
            return redirect('commande')
            
        except Exception as e:
            if order:
                order.delete()
            return render(request, 'Panier/panier.html', {
                'items': items,
                'total': sum(item.product.price * item.quantity for item in items),
                'error': 'Une erreur est survenue lors du traitement de la commande'
            })

    return render(request, 'Panier/panier.html', {
        'items': items,
        'total': sum(item.product.price * item.quantity for item in items)
    })

# View orders

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    for order in orders:
        order.items_count = order.items.count()
        order.items_list = order.items.all()
        
        payment = Payment.objects.filter(order=order).first()
        order.payment_info = payment
        
        # Statut
        if payment and payment.status == 'COMPLETED':
            order.status = 'Payée'
            order.status_color = 'success'
        else:
            order.status = 'En attente'
            order.status_color = 'warning'
        
        # Mode de paiement
        order.mode_paiement = payment.method if payment else "N/A"

        # Montant total
        order.montant_total = sum(item.price * item.quantity for item in order.items_list)

        # Numéro de commande
        order.numero = order.id  # ou un champ unique si défini dans ton modèle

        # Date de commande et livraison
        order.date_commande = order.created_at
        order.date_livraison = order.delivery_date if hasattr(order, 'delivery_date') else None

    return render(request, 'Commande/commande.html', {
        'commandes': orders,  # ⬅ On garde "commandes" pour correspondre au template
        'total_orders': orders.count()
    })


# User login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'conn/connect.html', {'error': 'Veuillez remplir tous les champs'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('index')
        else:
            return render(request, 'conn/connect.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
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
        
        if not username or not password or not email:
            return render(request, 'conn/inscript.html', {'error': 'Veuillez remplir tous les champs'})
            
        if User.objects.filter(username=username).exists():
            return render(request, 'conn/inscript.html', {'error': 'Ce nom d\'utilisateur existe déjà'})
            
        if User.objects.filter(email=email).exists():
            return render(request, 'conn/inscript.html', {'error': 'Cette adresse email est déjà utilisée'})
            
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('index')
        except Exception as e:
            return render(request, 'conn/inscript.html', {'error': 'Une erreur est survenue lors de l\'inscription'})
            
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