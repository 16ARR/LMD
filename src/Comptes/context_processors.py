from .models import CustomUser

def get_user_profile(request):
    if request.user.is_authenticated:
        # request.user is already the instance of CustomUser if you're using it as AUTH_USER_MODEL
        return {'user_profile': request.user}
    return {'user_profile': None}