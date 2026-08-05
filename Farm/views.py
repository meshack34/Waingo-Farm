from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Order
from .mpesa import initiate_stk_push
from django.contrib import messages
from .models import Category, Product, Order, OrderItem




from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from .models import (
    Category,
    Product,
    Order,
    OrderItem,
)

from .forms import CheckoutForm


def home(request):

    return render(
        request,
        "home.html"
    )


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


# =========================================================
# CART
# =========================================================

def add_to_cart(request, product_id):

    if request.method != "POST":
        return redirect("shop")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    quantity = int(
        request.POST.get(
            "quantity",
            1
        )
    )

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        quantity = product.stock

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product.id)

    if product_id in cart:

        cart[product_id] += quantity

    else:

        cart[product_id] = quantity

    request.session["cart"] = cart

    request.session.modified = True

    messages.success(
        request,
        f"{product.name} has been added to your cart."
    )

    return redirect(
        "product_detail",
        slug=product.slug
    )


def cart(request):

    cart = request.session.get(
        "cart",
        {}
    )

    cart_items = []

    total = 0

    for product_id, quantity in cart.items():

        try:

            product = Product.objects.get(
                id=product_id,
                is_available=True
            )

        except Product.DoesNotExist:

            continue

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({

            "product": product,

            "quantity": quantity,

            "subtotal": subtotal,

        })


    context = {

        "cart_items": cart_items,

        "cart_total": total,

    }

    return render(
        request,
        "cart.html",
        context
    )


def update_cart(request, product_id):

    if request.method != "POST":
        return redirect("cart")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    quantity = int(
        request.POST.get(
            "quantity",
            1
        )
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product.id)

    if quantity <= 0:

        cart.pop(
            product_id,
            None
        )

    else:

        if quantity > product.stock:
            quantity = product.stock

        cart[product_id] = quantity


    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    cart.pop(
        product_id,
        None
    )

    request.session["cart"] = cart

    request.session.modified = True

    messages.info(
        request,
        "Product removed from your cart."
    )

    return redirect("cart")






def checkout(request):

    cart = request.session.get(
        "cart",
        {}
    )

    if not cart:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("shop")


    cart_items = []

    cart_total = Decimal("0.00")


    for product_id, quantity in cart.items():

        try:

            product = Product.objects.get(
                id=product_id,
                is_available=True
            )

        except Product.DoesNotExist:

            continue


        # Make sure requested quantity is still available

        if quantity > product.stock:

            quantity = product.stock


        if quantity <= 0:

            continue


        subtotal = product.price * quantity

        cart_total += subtotal


        cart_items.append({

            "product": product,

            "quantity": quantity,

            "subtotal": subtotal,

        })


    if not cart_items:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("shop")


    if request.method == "POST":

        form = CheckoutForm(
            request.POST
        )

        if form.is_valid():

            order = form.save(
                commit=False
            )

            order.total_amount = cart_total

            order.status = "pending"

            order.save()


            # Create order items

            for item in cart_items:

                OrderItem.objects.create(

                    order=order,

                    product=item["product"],

                    quantity=item["quantity"],

                    price=item["product"].price,

                )


            # We will clear the cart after
            # successful payment later.
            #
            # For now, keep it until M-Pesa
            # integration is completed.

            request.session["pending_order_id"] = order.id

            request.session.modified = True


            return redirect(
                "payment",
                order_id=order.id
            )


    else:

        form = CheckoutForm()


    context = {

        "form": form,

        "cart_items": cart_items,

        "cart_total": cart_total,

    }


    return render(
        request,
        "checkout.html",
        context
    )

def payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        phone_number = request.POST.get("phone", "").strip()

        # Remove spaces
        phone_number = phone_number.replace(" ", "")

        # Convert +254712345678 → 254712345678
        if phone_number.startswith("+254"):
            phone_number = phone_number[1:]

        # Convert 0712345678 → 254712345678
        elif phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]

        # Validate Kenyan number
        if (
            not phone_number.startswith("254")
            or len(phone_number) != 12
            or not phone_number.isdigit()
        ):
            messages.error(
                request,
                "Please enter a valid Kenyan M-Pesa phone number."
            )

            return render(
                request,
                "payment.html",
                {
                    "order": order
                }
            )

        try:

            response = initiate_stk_push(
                phone_number=phone_number,
                amount=order.total_amount,
                account_reference=f"ORDER-{order.id}",
                transaction_description="Waingo Farm Order Payment",
            )

            if response.get("ResponseCode") == "0":

                # Save M-Pesa request information
                order.mpesa_merchant_request_id = response.get(
                    "MerchantRequestID"
                )

                order.mpesa_checkout_request_id = response.get(
                    "CheckoutRequestID"
                )

                order.save(
                    update_fields=[
                        "mpesa_merchant_request_id",
                        "mpesa_checkout_request_id",
                    ]
                )

                messages.success(
                    request,
                    "M-Pesa payment request sent. "
                    "Please check your phone and enter your M-Pesa PIN."
                )

                return render(
                    request,
                    "payment.html",
                    {
                        "order": order,
                        "stk_sent": True,
                    }
                )

            messages.error(
                request,
                response.get(
                    "errorMessage",
                    "Unable to initiate M-Pesa payment."
                )
            )

        except Exception as e:

            messages.error(
                request,
                f"Payment request failed: {str(e)}"
            )

    return render(
        request,
        "payment.html",
        {
            "order": order
        }
    )