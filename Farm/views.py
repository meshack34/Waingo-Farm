from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def home(request):
    return render(request, "home.html")


def shop(request):

    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
    }

    return render(
        request,
        "shop.html",
        context
    )


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    return render(
        request,
        "product_detail.html",
        {
            "product": product
        }
    )