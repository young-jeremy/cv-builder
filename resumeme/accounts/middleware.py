from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.contrib import messages


class EnsureUserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Skip this check for the create_profile view and related URLs
            current_url = resolve(request.path_info).url_name
            exempt_urls = ['create_profile', 'logout', 'admin:index', 'admin:login']

            if current_url not in exempt_urls and not request.path.startswith('/admin/'):
                try:
                    # Try to access the profile
                    profile = request.user.profile
                except:
                    # If we're not already on the create_profile page, redirect there
                    if current_url != 'create_profile':
                        messages.info(request, "Please complete your profile information.")
                        return redirect('create_profile')

        response = self.get_response(request)
        return response

