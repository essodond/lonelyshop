from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produits/', views.product_list, name='produit'),
    path('produit/<int:product_id>/', views.product_detail, name='produit_detail'),
    path('ajouter_panier/', views.add_to_cart, name='ajouter_panier'),
    path('panier/', views.view_cart, name='panier'),
    path('panier/supprimer/<int:item_id>/', views.remove_from_cart, name='supprimer_panier'),
    path('commande/', views.view_orders, name='commande'),
    path('commande/placer/', views.place_order, name='placer_commande'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('api/cart-quantity/', views.cart_quantity_api, name='cart_quantity_api'),


]