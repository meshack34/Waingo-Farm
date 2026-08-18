from django.urls import include, path
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
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("gallery/", views.gallery, name="gallery"),

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
    path( "payment/status/<int:order_id>/",
        views.payment_status,
        name="payment_status"
    ),
    path(
    "payment/success/<int:order_id>/",
    views.payment_success,
    name="payment_success"
),
    path(
        "mpesa/callback/",
        views.mpesa_callback,
        name="mpesa_callback",
    ),

path("owner/", include("Farm.owner.urls")),
]