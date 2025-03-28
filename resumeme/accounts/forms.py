from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """Form for updating users."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'bio', 'profile_picture', 'date_of_birth', 'phone_number')


class UserProfileForm(forms.ModelForm):
    """Form for updating user profiles."""

    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'state', 'country', 'postal_code')


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


