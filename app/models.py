from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sizes = models.CharField(max_length=100, default='S,M,L,XL,XXL', blank=True)


    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CARD', 'Carte bancaire'),
        ('MIXX', 'Mixx by yass'),
        ('FLOOZ', 'Flooz Money')
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'En attente'),
        ('PROCESSING', 'En cours'),
        ('COMPLETED', 'Complété'),
        ('FAILED', 'Échoué')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    payment_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_cvv = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"Paiement {self.get_method_display()} - {self.order.id}"
