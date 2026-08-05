from decimal import Decimal

from .models import Product


def cart_context(request):

    cart = request.session.get(
        "cart",
        {}
    )

    cart_count = 0

    cart_total = Decimal("0.00")


    for product_id, quantity in cart.items():

        try:

            product = Product.objects.get(
                id=product_id,
                is_available=True
            )

        except Product.DoesNotExist:

            continue


        cart_count += quantity

        cart_total += (
            product.price * quantity
        )


    return {

        "cart_count": cart_count,

        "cart_total": cart_total,

    }