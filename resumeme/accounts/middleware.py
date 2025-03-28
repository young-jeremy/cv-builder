from django.shortcuts import redirect
from django.contrib import messages
from .models import LoginAttempt
from django.core.cache import cache


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for suspicious activity
        ip_address = self.get_client_ip(request)

        # Rate limiting
        if self.is_rate_limited(ip_address):
            messages.error(request, 'Too many requests. Please try again later.')
            return redirect('login')

        # Track login attempts
        if request.path == '/login/' and request.method == 'POST':
            self.track_login_attempt(request, ip_address)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_rate_limited(self, ip):
        key = f'rate_limit_{ip}'
        attempts = cache.get(key, 0)
        if attempts >= 5:  # 5 attempts per minute
            return True
        cache.set(key, attempts + 1, 60)  # 60 seconds expiry
        return False

    def track_login_attempt(self, request, ip):
        if hasattr(request, 'user') and request.user.is_authenticated:
            LoginAttempt.objects.create(
                user=request.user,
                ip_address=ip,
                was_successful=True,
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )