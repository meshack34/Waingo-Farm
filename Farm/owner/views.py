from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.db.models import F

from Farm.models import (
    Product,
    Category,
    Order,
    OrderItem,
)

from Farm.models import OrderItem

from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from Farm.models import (
    Product,
    Category,
    Order,
)

from .forms import ProductForm


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "owner/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_products"] = Product.objects.count()

        context["available_products"] = Product.objects.filter(
            is_available=True
        ).count()

        context["pending_orders"] = Order.objects.filter(
            status="pending"
        ).count()

        context["paid_orders"] = Order.objects.filter(
            status="paid"
        ).count()

        context["total_sales"] = (
            Order.objects.filter(status="paid")
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        context["recent_orders"] = Order.objects.order_by(
            "-created_at"
        )[:5]

        context["low_stock_products"] = Product.objects.filter(
            stock__lte=10,
            stock__gt=0,
        )

        return context


class ProductListView(LoginRequiredMixin, ListView):

    model = Product

    template_name = "owner/products/products.html"

    context_object_name = "products"

    paginate_by = 12

    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()

        return context


class ProductCreateView(

    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):

    model = Product

    form_class = ProductForm

    template_name = "owner/products/product_form.html"

    success_url = reverse_lazy("owner:products")

    success_message = "Product added successfully."


class ProductUpdateView(

    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):

    model = Product

    form_class = ProductForm

    template_name = "owner/products/product_form.html"

    success_url = reverse_lazy("owner:products")

    success_message = "Product updated successfully."


class ProductDeleteView(

    LoginRequiredMixin,
    DeleteView,
):

    model = Product

    template_name = "owner/products/product_delete.html"

    success_url = reverse_lazy("owner:products")


class OrderListView(LoginRequiredMixin, ListView):

    model = Order

    template_name = "owner/orders/orders.html"

    context_object_name = "orders"

    paginate_by = 12

    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["pending_orders"] = Order.objects.filter(
            status="pending"
        ).count()

        context["paid_orders"] = Order.objects.filter(
            status="paid"
        ).count()

        context["delivered_orders"] = Order.objects.filter(
            status="delivered"
        ).count()

        context["cancelled_orders"] = Order.objects.filter(
            status="cancelled"
        ).count()

        context["counties"] = (
            Order.objects
            .values_list("county", flat=True)
            .distinct()
            .order_by("county")
        )

        return context


class OrderDetailView(LoginRequiredMixin, TemplateView):

    template_name = "owner/orders/order_detail.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        order = get_object_or_404(
            Order,
            pk=self.kwargs["pk"]
        )

        context["order"] = order

        context["items"] = OrderItem.objects.filter(
            order=order
        ).select_related("product")

        return context



class AnalyticsView(TemplateView):

    template_name = "owner/analytics/analytics.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_revenue"] = (
            Order.objects.filter(status="paid")
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        context["total_orders"] = Order.objects.count()

        context["total_customers"] = (
            Order.objects.values("phone").distinct().count()
        )

        context["total_products_sold"] = (
            OrderItem.objects.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        )

        monthly_sales = (
            Order.objects.filter(status="paid")
            .annotate(month=TruncMonth("paid_at"))
            .values("month")
            .annotate(total=Sum("total_amount"))
            .order_by("month")
        )

        context["revenue_labels"] = [
            sale["month"].strftime("%b")
            for sale in monthly_sales
            if sale["month"]
        ]

        context["revenue_values"] = [
            float(sale["total"])
            for sale in monthly_sales
        ]

        statuses = ["pending", "paid", "delivered", "cancelled"]

        context["status_labels"] = [
            s.title() for s in statuses
        ]

        context["status_values"] = [
            Order.objects.filter(status=s).count()
            for s in statuses
        ]

        context["best_products"] = (
            Product.objects.annotate(
                total_sold=Sum("order_items__quantity")
            )
            .order_by("-total_sold")[:5]
        )

        context["low_stock_products"] = (
            Product.objects.filter(
                stock__lte=F("low_stock_threshold")
            )
            .order_by("stock")[:5]
        )

        context["recent_payments"] = (
            Order.objects.filter(
                status="paid"
            )
            .order_by("-paid_at")[:10]
        )

        return context