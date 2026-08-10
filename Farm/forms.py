from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [
            "full_name",
            "phone",
            "email",
            "county",
            "town",
            "delivery_address",
            "order_notes",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 0712345678",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "your@email.com",
                }
            ),

            "county": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Kenya",
                }
            ),

            "town": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Karen",
                }
            ),

            "delivery_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your delivery address",
                }
            ),

            "order_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Any special instructions? (Optional)",
                }
            ),
        }