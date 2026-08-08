from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name_plural = "Categories"

        ordering = ["name"]


    def __str__(self):

        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            kwargs={"slug": self.slug}
        )

    @property
    def is_low_stock(self):
        return self.stock <= 5

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=30
    )

    email = models.EmailField(
        blank=True
    )

    county = models.CharField(
        max_length=100
    )

    town = models.CharField(
        max_length=100
    )

    delivery_address = models.TextField()

    order_notes = models.TextField(
        blank=True
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

        # =========================================================
    # MPESA PAYMENT DETAILS
    # =========================================================

    mpesa_merchant_request_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    mpesa_checkout_request_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    mpesa_receipt_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    mpesa_result_code = models.IntegerField(
        blank=True,
        null=True
    )

    mpesa_result_description = models.TextField(
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):

        return f"Order #{self.id} - {self.full_name}"

    class Meta:

        ordering = ["-created_at"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity 
    
    @property
    def subtotal(self):
        return self.quantity * self.price
