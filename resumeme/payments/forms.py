from django import forms
from django.utils import timezone

from .models import Plan


class PlanSelectionForm(forms.Form):
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.filter(is_active=True),
        widget=forms.RadioSelect,
        empty_label=None
    )


class PaymentForm(forms.Form):
    name_on_card = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name on card'
    }))

    # These fields would be handled by Stripe.js in the frontend
    # We're including them here for form validation
    card_number = forms.CharField(max_length=19, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Card number',
        'data-stripe': 'number'
    }))

    expiry_month = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-select', 'data-stripe': 'exp-month'})
    )

    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(timezone.now().year, timezone.now().year + 15)],
        widget=forms.Select(attrs={'class': 'form-select', 'data-stripe': 'exp-year'})
    )

    cvc = forms.CharField(max_length=4, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'CVC',
        'data-stripe': 'cvc'
    }))