from django import forms

from Farm.models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = (
            "category",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "stock",
            "is_available",
            "is_featured",
        )

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product name",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "product-slug",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Write a short product description...",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "is_available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = (
            "name",
            "slug",
            "description",
            "image",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category name",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "category-slug",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe this category...",
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }



        # ============================================================
# PROFILE FORM
# ============================================================

from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Enter username",
                    "autocomplete": "username",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter first name",
                    "autocomplete": "given-name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter last name",
                    "autocomplete": "family-name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter email address",
                    "autocomplete": "email",
                }
            ),
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if not username:
            raise forms.ValidationError(
                "Username cannot be empty."
            )

        queryset = User.objects.filter(
            username__iexact=username
        ).exclude(
            pk=self.instance.pk
        )

        if queryset.exists():
            raise forms.ValidationError(
                "This username is already in use."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()

        return email