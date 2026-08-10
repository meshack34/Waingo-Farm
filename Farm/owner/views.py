from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import (
    ProductForm,
    CategoryForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.shortcuts import render, redirect

from Farm.models import (
    Product,
    Category,
    Order,
    OrderItem,
)

from .forms import (
    ProductForm,
    CategoryForm,
)


# ============================================================
# DASHBOARD
# ============================================================

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

        context["recent_orders"] = (
            Order.objects
            .order_by("-created_at")[:5]
        )


        context["low_stock_products"] = (
            Product.objects
            .filter(
                stock__lte=10,
                stock__gt=0,
            )
        )

        return context


# ============================================================
# PRODUCTS
# ============================================================

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


# ============================================================
# ORDERS
# ============================================================

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
            status="completed"
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
            pk=self.kwargs["pk"],
        )

        context["order"] = order

        context["items"] = (
            OrderItem.objects
            .filter(order=order)
            .select_related("product")
        )

        return context


# ============================================================
# ANALYTICS
# ============================================================

class AnalyticsView(LoginRequiredMixin, TemplateView):

    template_name = "owner/analytics/analytics.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_revenue"] = (
            Order.objects
            .filter(status="paid")
            .aggregate(total=Sum("total_amount"))["total"] or 0
        )

        context["total_orders"] = Order.objects.count()

        context["total_customers"] = (
            Order.objects
            .values("phone")
            .distinct()
            .count()
        )

        context["total_products_sold"] = (
            OrderItem.objects
            .aggregate(total=Sum("quantity"))["total"] or 0
        )

        monthly_sales = (
            Order.objects
            .filter(status="paid")
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

        statuses = [
            "pending",
            "paid",
            "completed",
            "cancelled",
        ]

        context["status_labels"] = [
            status.title()
            for status in statuses
        ]

        context["status_values"] = [
            Order.objects
            .filter(status=status)
            .count()
            for status in statuses
        ]

        context["best_products"] = (
            Product.objects
            .annotate(
                total_sold=Sum("orderitem__quantity")
            )
            .order_by("-total_sold")[:5]
        )

        # Low stock products
        context["low_stock_products"] = (
            Product.objects
            .filter(
                stock__lte=10,
                stock__gt=0
            )
            .order_by("stock")[:5]
        )

    

        context["recent_payments"] = (
            Order.objects
            .filter(status="paid")
            .order_by("-paid_at")[:10]
        )

        return context


# ============================================================
# CATEGORIES
# ============================================================

class CategoryListView(LoginRequiredMixin, ListView):

    model = Category

    template_name = "owner/categories/categories.html"

    context_object_name = "categories"

    paginate_by = 12

    ordering = ["name"]


class CategoryCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):

    model = Category

    form_class = CategoryForm

    template_name = "owner/categories/category_form.html"

    success_url = reverse_lazy("owner:categories")

    success_message = "Category added successfully."


class CategoryUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):

    model = Category

    form_class = CategoryForm

    template_name = "owner/categories/category_form.html"

    success_url = reverse_lazy("owner:categories")

    success_message = "Category updated successfully."


class CategoryDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Category
    template_name = "owner/categories/category_delete.html"
    success_url = reverse_lazy("owner:categories")
    success_message = "Category deleted successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["product_count"] = self.object.products.count()

        return context

    # ============================================================
# PROFILE
# ============================================================

@login_required
def profile(request):
    return render(
        request,
        "owner/profile/profile.html",
        {
            "profile_user": request.user,
        }
    )


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully."
            )

            return redirect("owner:profile")

    else:
        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "owner/profile/profile_edit.html",
        {
            "form": form,
        }
    )


# ============================================================
# SETTINGS
# ============================================================

@login_required
def settings(request):
    return render(
        request,
        "owner/settings/settings.html",
    )