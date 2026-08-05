import base64
import requests

from datetime import datetime

from django.conf import settings


def get_mpesa_access_token():

    url = (
        "https://sandbox.safaricom.co.ke/oauth/"
        "v1/generate?grant_type=client_credentials"
    )

    response = requests.get(
        url,
        auth=(
            settings.DARAJA_CONSUMER_KEY,
            settings.DARAJA_CONSUMER_SECRET,
        ),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def generate_password(timestamp):

    data = (
        f"{settings.DARAJA_SHORTCODE}"
        f"{settings.DARAJA_PASSKEY}"
        f"{timestamp}"
    )

    encoded = base64.b64encode(
        data.encode()
    ).decode()

    return encoded


def initiate_stk_push(
    phone_number,
    amount,
    account_reference,
    transaction_description,
):

    access_token = get_mpesa_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = generate_password(timestamp)

    url = (
        "https://sandbox.safaricom.co.ke/"
        "mpesa/stkpush/v1/processrequest"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": settings.DARAJA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": settings.DARAJA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.DARAJA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_description,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30,
    )

    print("\n========================================")
    print("MPESA STATUS CODE:", response.status_code)
    print("MPESA RESPONSE:", response.text)
    print("========================================\n")

    if not response.ok:
        return {
            "success": False,
            "status_code": response.status_code,
            "response": response.text,
        }

    return response.json()