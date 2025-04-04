from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_user_avatar_url(user):
    """
    Returns the URL of the user's avatar or None if not set
    """
    try:
        if user.profile.avatar:
            return user.profile.avatar.url
        return None
    except:
        return None

@register.simple_tag
def get_user_initials(user):
    """
    Returns the user's initials based on first and last name
    """
    initials = ""
    if user.first_name:
        initials += user.first_name[0].upper()
    if user.last_name:
        initials += user.last_name[0].upper()
    if not initials and user.username:
        initials = user.username[0].upper()
    return initials

@register.filter
def is_premium_user(user):
    """
    Checks if a user has premium access
    """
    try:
        return user.profile.has_premium_access
    except:
        return False

