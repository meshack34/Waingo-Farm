from django.urls import path

from .views import (
    DashboardView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)
from .views import (
    DashboardView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderListView,
    OrderDetailView,
)

app_name = "owner"

urlpatterns = [

    # Dashboard
    path(
        "",
        DashboardView.as_view(),
        name="dashboard",
    ),

    # Products
    path(
        "products/",
        ProductListView.as_view(),
        name="products",
    ),

    path(
        "products/add/",
        ProductCreateView.as_view(),
        name="product_add",
    ),

    path(
        "products/<int:pk>/edit/",
        ProductUpdateView.as_view(),
        name="product_edit",
    ),

    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),


# Orders

path(
    "orders/",
    OrderListView.as_view(),
    name="orders",
),

path(
    "orders/<int:pk>/",
    OrderDetailView.as_view(),
    name="order_detail",
),
]