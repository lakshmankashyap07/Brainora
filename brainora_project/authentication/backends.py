from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend to allow login with either username or email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Get the user model dynamically to avoid AppRegistryNotReady issues
        User = get_user_model()
        try:
            # Check if the user exists with the given username OR email
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None