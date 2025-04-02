from django import forms
from .models import TemplateCategory, ResumeTemplate


class TemplateFilterForm(forms.Form):
    """Form for filtering resume templates"""
    PHOTO_CHOICES = [
        ('', 'Any'),
        ('true', 'With Photo'),
        ('false', 'Without Photo'),
    ]

    PREMIUM_CHOICES = [
        ('', 'Any'),
        ('false', 'Free'),
        ('true', 'Premium'),
    ]

    category = forms.ModelChoiceField(
        queryset=TemplateCategory.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ats_friendly = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    has_photo = forms.ChoiceField(
        choices=PHOTO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    premium = forms.ChoiceField(
        choices=PREMIUM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search templates...'
        })
    )


class ColorSchemeForm(forms.Form):
    """Form for selecting a color scheme"""
    color_scheme = forms.ChoiceField(
        choices=[],  # Will be populated dynamically
        widget=forms.RadioSelect(attrs={'class': 'color-radio'})
    )

    def __init__(self, template, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices with color schemes for the template
        self.fields['color_scheme'].choices = [
            (color.id, color.name) for color in template.colors.all()
        ]

