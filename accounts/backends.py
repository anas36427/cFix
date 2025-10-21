# from django.contrib.auth.backends import ModelBackend
# from .models import CustomUser

# class CollegeIdBackend(ModelBackend):
#     def authenticate(self, request, college_id=None, password=None, **kwargs):
#         try:
#             user = CustomUser.objects.get(college_id=college_id)
#             if user.check_password(password):
#                 return user
#         except CustomUser.DoesNotExist:
#             return None
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CollegeIdBackend(ModelBackend):

    def authenticate(self, request, college_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(college_id=college_id)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
