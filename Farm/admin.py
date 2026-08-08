from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Product,
    Order,
    OrderItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    "image_preview",
    "name",
    "category",
    "price",
    "stock_status",
    "available_status",
    "featured_status",
    "created_at",
)

    list_filter = (
        "category",
        "is_available",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "category__name",
    )

    list_editable = (
        "price",
    )

    list_per_page = 20

    ordering = (
        "-created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:8px; object-fit:cover;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Image"

    def stock_status(self, obj):
        if obj.stock == 0:
            color = "#dc3545"
            text = "Out of Stock"
        elif obj.is_low_stock:
            color = "#fd7e14"
            text = f"Low ({obj.stock})"
        else:
            color = "#198754"
            text = f"In Stock ({obj.stock})"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            text,
        )

    stock_status.short_description = "Stock"


    def available_status(self, obj):
        if obj.is_available:
            return format_html(
                '<span style="color:#198754;font-weight:600;">✓ Available</span>'
            )

        return format_html(
            '<span style="color:#dc3545;font-weight:600;">✗ Unavailable</span>'
        )

    available_status.short_description = "Available"


    def featured_status(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="color:#0d6efd;font-weight:600;">★ Featured</span>'
            )

        return format_html(
            '<span style="color:#6c757d;">—</span>'
        )

    featured_status.short_description = "Featured"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "phone",
        "county",
        "town",
        "total_amount",
        "status",
        "mpesa_receipt_number",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "status",
        "county",
        "created_at",
        "paid_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "mpesa_receipt_number",
        "mpesa_checkout_request_id",
        "mpesa_merchant_request_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "mpesa_merchant_request_id",
        "mpesa_checkout_request_id",
        "mpesa_receipt_number",
        "mpesa_result_code",
        "mpesa_result_description",
        "paid_at",
    )

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "email",
                    "county",
                    "town",
                    "delivery_address",
                    "order_notes",
                )
            },
        ),

        (
            "Order Information",
            {
                "fields": (
                    "total_amount",
                    "status",
                )
            },
        ),

        (
            "M-Pesa Payment",
            {
                "fields": (
                    "mpesa_merchant_request_id",
                    "mpesa_checkout_request_id",
                    "mpesa_receipt_number",
                    "mpesa_result_code",
                    "mpesa_result_description",
                    "paid_at",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )