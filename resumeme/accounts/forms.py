from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from .models import UserProfile


class UserForm(forms.ModelForm):
    """Form for updating basic User model fields"""
    first_name = forms.CharField(
        max_length=30,
        required=True,  # Make this required for profile creation
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,  # Make this required for profile creation
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if this is an existing user (has an ID)
        if self.instance.pk:
            # Exclude the current user by ID, not username
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Email address is already in use.')
        else:
            # For new users, just check if email exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Email address is already in use.')

        return email


class UserProfileForm(forms.ModelForm):
    """Form for updating UserProfile model fields"""
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself'  'form-control',
            'rows': 4,
            'placeholder': 'Tell us about yourself'
        })
    )

    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., New York, NY'
    }))

    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., +1 (555) 123-4567'
    }))

    website = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://example.com'
    }))

    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://linkedin.com/in/username'
    }))

    github_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://github.com/username'
    }))

    twitter_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://twitter.com/username'
    }))

    # Address fields
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 2,
        'placeholder': 'Street address'
    }))

    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))

    state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State/Province'
    }))

    country = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Country'
    }))

    postal_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Postal/ZIP Code'
    }))

    # Professional information
    job_title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., Software Engineer'
    }))

    company = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., Acme Inc.'
    }))

    # Preferences
    email_notifications = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))

    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'location', 'phone',
            'website', 'linkedin_url', 'github_url', 'twitter_url',
            'address', 'city', 'state', 'country', 'postal_code',
            'job_title', 'company', 'email_notifications'
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """Form for updating users."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile picture and phone number."""

    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone']
        labels = {
            'avatar': 'Profile Picture',
            'phone': 'Phone Number'
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class SecurityQuestionForm(forms.Form):
    QUESTIONS = [
        ('pet', 'What was your first pet''s name?'),
        ('school', 'What was the name of your first school?'),
        ('city', 'In which city were you born?'), ]
    question = forms.ChoiceField(choices=QUESTIONS)
    answer = forms.CharField(max_length=200)





class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


