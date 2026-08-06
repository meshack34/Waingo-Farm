from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from .mpesa import initiate_stk_push
from django.contrib import messages
from .models import Category, Product, Order, OrderItem
import json
from django.http import JsonResponse
from django.utils import timezone




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

def services(request):

    return render(
        request,
        "services.html"
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

        # =====================================================
        # GET PHONE NUMBER
        # =====================================================

        phone_number = request.POST.get(
            "phone",
            ""
        ).strip()

        print("========================================")
        print("PAYMENT POST RECEIVED")
        print("PHONE FROM FORM:", phone_number)
        print("ORDER ID:", order.id)
        print("ORDER AMOUNT:", order.total_amount)
        print("========================================")

        # Remove spaces
        phone_number = phone_number.replace(" ", "")

        # Remove hyphen if someone enters one
        phone_number = phone_number.replace("-", "")

        # =====================================================
        # NORMALIZE KENYAN PHONE NUMBER
        # =====================================================

        # 0712345678 → 254712345678
        if phone_number.startswith("0"):

            phone_number = (
                "254"
                + phone_number[1:]
            )

        # +254712345678 → 254712345678
        elif phone_number.startswith("+254"):

            phone_number = phone_number[1:]

        # 712345678 → 254712345678
        elif (
            len(phone_number) == 9
            and phone_number.startswith("7")
        ):

            phone_number = (
                "254"
                + phone_number
            )

        print("NORMALIZED PHONE:", phone_number)

        # =====================================================
        # VALIDATE PHONE NUMBER
        # =====================================================

        if (
            len(phone_number) != 12
            or not phone_number.isdigit()
            or not phone_number.startswith("2547")
        ):

            print("INVALID PHONE NUMBER:", phone_number)

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

        # =====================================================
        # INITIATE STK PUSH
        # =====================================================

        try:

            print("========================================")
            print("CALLING MPESA STK PUSH")
            print("PHONE SENT TO MPESA:", phone_number)
            print("AMOUNT SENT TO MPESA:", order.total_amount)
            print("========================================")

            response = initiate_stk_push(

                phone_number=phone_number,

                amount=order.total_amount,

                account_reference=(
                    f"ORDER-{order.id}"
                ),

                transaction_description=(
                    "Waingo Farm Order Payment"
                ),

            )

            print("========================================")
            print("MPESA FUNCTION RETURNED")
            print("MPESA RESPONSE FROM VIEW:", response)
            print("========================================")

            # =================================================
            # SUCCESSFUL STK REQUEST
            # =================================================

            if response.get("ResponseCode") == "0":

                order.mpesa_merchant_request_id = (
                    response.get(
                        "MerchantRequestID"
                    )
                )

                order.mpesa_checkout_request_id = (
                    response.get(
                        "CheckoutRequestID"
                    )
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
                    "Please check your phone and "
                    "enter your M-Pesa PIN."
                )

                return render(
                    request,
                    "payment.html",
                    {
                        "order": order,
                        "stk_sent": True,
                    }
                )

            # =================================================
            # SAFARICOM RETURNED AN ERROR
            # =================================================

            error_message = response.get(
                "errorMessage",
                response.get(
                    "ResponseDescription",
                    "Unable to initiate M-Pesa payment."
                )
            )

            print(
                "MPESA REQUEST FAILED:",
                error_message
            )

            messages.error(
                request,
                error_message
            )

        # =====================================================
        # PYTHON / REQUEST ERROR
        # =====================================================

        except Exception as e:

            print("========================================")
            print("MPESA ERROR")
            print(repr(e))
            print("========================================")

            messages.error(
                request,
                f"Payment request failed: {str(e)}"
            )

    # =========================================================
    # GET REQUEST
    # =========================================================

    return render(
        request,
        "payment.html",
        {
            "order": order
        }
    )
    
@csrf_exempt
def mpesa_callback(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "ResultCode": 1,
                "ResultDesc": "Method not allowed",
            },
            status=405,
        )

    try:
        data = json.loads(request.body)

        print("\n===================================")
        print("MPESA CALLBACK RECEIVED")
        print(json.dumps(data, indent=4))
        print("===================================\n")

        stk_callback = (
            data
            .get("Body", {})
            .get("stkCallback", {})
        )

        merchant_request_id = stk_callback.get(
            "MerchantRequestID"
        )

        checkout_request_id = stk_callback.get(
            "CheckoutRequestID"
        )

        result_code = stk_callback.get(
            "ResultCode"
        )

        result_description = stk_callback.get(
            "ResultDesc"
        )

        print("MerchantRequestID:", merchant_request_id)
        print("CheckoutRequestID:", checkout_request_id)
        print("ResultCode:", result_code)
        print("ResultDesc:", result_description)

        # -------------------------------------------------
        # Validate callback
        # -------------------------------------------------

        if not checkout_request_id:
            print("Missing CheckoutRequestID")

            return JsonResponse(
                {
                    "ResultCode": 0,
                    "ResultDesc": "Accepted",
                }
            )

        # -------------------------------------------------
        # Find order
        # -------------------------------------------------

        order = Order.objects.filter(
            mpesa_checkout_request_id=checkout_request_id
        ).first()

        if not order:

            print(
                "Order not found for CheckoutRequestID:",
                checkout_request_id
            )

            return JsonResponse(
                {
                    "ResultCode": 0,
                    "ResultDesc": "Accepted",
                }
            )

        # -------------------------------------------------
        # Save basic callback information
        # -------------------------------------------------

        order.mpesa_merchant_request_id = merchant_request_id
        order.mpesa_checkout_request_id = checkout_request_id
        order.mpesa_result_code = result_code
        order.mpesa_result_description = result_description

        # -------------------------------------------------
        # PAYMENT SUCCESSFUL
        # -------------------------------------------------

        if result_code == 0:

            callback_metadata = stk_callback.get(
                "CallbackMetadata",
                {}
            )

            items = callback_metadata.get(
                "Item",
                []
            )

            metadata = {}

            for item in items:

                name = item.get("Name")
                value = item.get("Value")

                if name:
                    metadata[name] = value

            print("M-PESA METADATA:", metadata)

            # Receipt number
            order.mpesa_receipt_number = metadata.get(
                "MpesaReceiptNumber"
            )

            # Payment date/time
            order.paid_at = timezone.now()

            # Mark order as paid
            order.status = "paid"

            order.save()

            print(
                f"✅ ORDER #{order.id} MARKED AS PAID"
            )

        # -------------------------------------------------
        # PAYMENT FAILED / CANCELLED
        # -------------------------------------------------

        else:

            order.save()

            print(
                f"❌ ORDER #{order.id} PAYMENT FAILED"
            )

        # -------------------------------------------------
        # Tell Safaricom we received callback
        # -------------------------------------------------

        return JsonResponse(
            {
                "ResultCode": 0,
                "ResultDesc": "Accepted",
            }
        )

    except json.JSONDecodeError:

        print("❌ Invalid JSON received from M-Pesa")

        return JsonResponse(
            {
                "ResultCode": 1,
                "ResultDesc": "Invalid JSON",
            },
            status=400,
        )

    except Exception as e:

        print(
            "❌ MPESA CALLBACK ERROR:",
            repr(e)
        )

        return JsonResponse(
            {
                "ResultCode": 1,
                "ResultDesc": "Callback processing failed",
            },
            status=500,
        )