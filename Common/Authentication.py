
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
User = get_user_model()

import string
from django.utils.crypto import get_random_string

class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                Q(
                    Q(
                        Q(email=username)
                        # & Q(is_email_verified=True) # Remove to do email_verified in first Login
                    ) |
                    Q(
                        Q(phone=username) 
                        # & Q(is_phone_verified=True) # Remove to do phone_verified in first Login
                    ) |
                    Q(username=username)
                ) &
                Q(is_active = True)
            )

            if password != None:
                pwd_valid = user.check_password(password)
                if pwd_valid:
                    return user

            if password != None and  password != '':
                if user.otp == password:
                    user.otp = get_random_string(4, allowed_chars= string.digits)
                    if not user.is_phone_verified:
                        user.is_phone_verified = True # added to do phone_verified in first Login
                    user.save()
                    return user

            return None
        except User.DoesNotExist:
            return None
