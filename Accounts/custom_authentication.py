from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CustomEmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #Check if the username_or_email contains @ or not 
        #if it does authenticate on the basis of email otherwies on the basis of uesrname
        if '@' in username:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                # No user with this email address exists
                return None
        else:
            # Authenticate using username
            user = super().authenticate(request, username=username, password=password, **kwargs)
        
        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            return user
        else:
            # Invalid username/email or password
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
