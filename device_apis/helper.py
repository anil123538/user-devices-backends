from device_apis.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_user_from_token(request):
    token_header=JWTAuthentication().get_header(request)
    token=JWTAuthentication().get_raw_token(token_header)
    validated_token=JWTAuthentication().get_validated_token(token)
    user=JWTAuthentication().get_user(validated_token)
    user_obj=User.objects.get(username=User)
    print("user:",user_obj.first_name,user_obj.last_name,user_obj.username,user_obj.email,user_obj.pk)
    return user_obj
