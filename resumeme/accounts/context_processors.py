def user_profile(request):
    """
    Context processor to make user profile available in all templates
    """
    if request.user.is_authenticated:
        try:
            return {'user_profile': request.user.profile}
        except:
            return {'user_profile': None}
    return {'user_profile': None}

