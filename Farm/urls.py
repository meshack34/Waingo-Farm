from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Shop
    path(
        "shop/",
        views.shop,
        name="shop"
    ),

    # Product details
    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),

    # Cart
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # Add product to cart
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # Update cart item
    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="update_cart"
    ),

    # Remove cart item
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),
    path(
    "payment/<int:order_id>/",
    views.payment,
    name="payment"
),
    path(
        "mpesa/callback/",
        views.mpesa_callback,
        name="mpesa_callback",
    ),

]