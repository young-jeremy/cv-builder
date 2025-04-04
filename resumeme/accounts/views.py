from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    UserProfileForm, UserUpdateForm
)
from django.contrib.auth import login, authenticate

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import RegistrationForm, ProfileUpdateForm, SecurityQuestionForm
from .models import User, LoginAttempt
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import render, redirect, get_object_or_404

from django.db import transaction

from .models import UserProfile
from .forms import UserForm, UserProfileForm

from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    # Check if request.user exists and is authenticated
    if not request.user.is_authenticated:
        return redirect('account_login')

    try:
        # Get the user's profile or create it if it doesn't exist
        profile = request.user.profile
    except:
        # If there's an error with the profile, show a message
        messages.error(request, "There was an error accessing your profile.")
        return redirect('accounts:create_profile')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
def create_profile(request):
    """
    View for creating a new profile if one doesn't exist.
    """
    # Check if profile already exists
    if hasattr(request.user, 'profile'):
        messages.info(request, "You already have a profile.")
        return redirect('accounts:profile_view')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    # Create the profile but don't save it yet
                    profile = profile_form.save(commit=False)
                    profile.user = request.user  # Assign the user
                    profile.save()  # Now save it

                messages.success(request, 'Your profile has been created successfully!')
                return redirect('accounts:profile_view')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_new_profile': True,
    }
    return render(request, 'accounts/create_profile.html', context)


@login_required
def profile_edit(request):
    """View for editing the user's profile"""
    # Check if profile exists
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.info(request, "Please create your profile first.")
        return redirect('create_profile')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile_view')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_new_profile': False,
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def public_profile_view(request, username):
    """View for displaying a user's public profile"""
    user = get_object_or_404(User, username=username)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        messages.error(request, f"The user {username} has not created a profile yet.")
        return redirect('accounts:profile_view')

    # Check if the profile belongs to the current user
    is_own_profile = request.user == user

    context = {
        'profile_user': user,
        'profile': user_profile,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'accounts/public_profile.html', context)


@login_required
def delete_avatar(request):
    """View for deleting the user's avatar"""
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.avatar:
                profile.avatar.delete(save=True)
                messages.success(request, 'Your avatar has been removed.')
            else:
                messages.info(request, 'You do not have an avatar to remove.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Profile not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return redirect('profile_edit')


@login_required
def toggle_email_notifications(request):
    """View for toggling email notifications preference"""
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile.email_notifications = not profile.email_notifications
            profile.save()

            status = "enabled" if profile.email_notifications else "disabled"
            messages.success(request, f'Email notifications {status} successfully.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Profile not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return redirect('profile_edit')


@login_required
def update_settings(request):
    """
    View to handle updating user account settings.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = request.user
        user.username = username
        user.email = email

        if password:
            user.set_password(password)

        user.save()
        messages.success(request, 'Your account settings have been updated.')
        return redirect('accounts:update_settings')

    return render(request, 'accounts/settings.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User won't be able to login until email is verified
            user.save()

            # Send verification email
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.verification_token,
            })

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Please check your email to complete registration.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and str(user.verification_token) == token:
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now login.')
        return redirect('login')
    else:
        messages.error(request, 'The verification link was invalid or has expired.')
        return redirect('register')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard:dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home:index')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm, UserProfileForm


@login_required
def subscription_view(request):
    return render(request, 'accounts/subscription.html')

@login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')