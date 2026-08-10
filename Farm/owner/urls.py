from django.urls import path
from . import views

from .views import (
    DashboardView,

    # Products
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,

    # Orders
    OrderListView,
    OrderDetailView,

    # Analytics
    AnalyticsView,

    # Categories
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)


app_name = "owner"


urlpatterns = [

    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        "",
        DashboardView.as_view(),
        name="dashboard",
    ),


    # ========================================================
    # PRODUCTS
    # ========================================================

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


    # ========================================================
    # ORDERS
    # ========================================================

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


    # ========================================================
    # ANALYTICS
    # ========================================================

    path(
        "analytics/",
        AnalyticsView.as_view(),
        name="analytics",
    ),


    # ========================================================
    # CATEGORIES
    # ========================================================

    path(
        "categories/",
        CategoryListView.as_view(),
        name="categories",
    ),

    path(
        "categories/add/",
        CategoryCreateView.as_view(),
        name="category_add",
    ),

    path(
        "categories/<int:pk>/edit/",
        CategoryUpdateView.as_view(),
        name="category_edit",
    ),

    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),


    # ========================================================
    # PROFILE
    # ========================================================

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "profile/edit/",
        views.profile_edit,
        name="profile_edit",
    ),


    # ========================================================
    # SETTINGS
    # ========================================================

    path(
        "settings/",
        views.settings,
        name="settings",
    ),

]