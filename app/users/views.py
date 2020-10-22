from django.shortcuts import render
from rest_framework import status,generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from users.serializers import *
from users.services import UserService
#from users.authentications import ExpiringTokenAuthentication

from actstream import action

from datetime import datetime, timedelta
import pytz

class ObtainExpiringAuthToken(generics.CreateAPIView):
    """
    Given username and password it returns an access token for the api if it is superuser. No callback token authentication is required.
    This view could be used for admin logins.
    """
    authentication_classes=[]
    serializer_class=UsernamePasswordAuthSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = UserService.generate_token_for_user(serializer.validated_data['user'])
            return Response({'token': token.key})

        attempted_account=get_user_model().objects.filter(username=request.data['username']).first()
        if attempted_account is not None:
            action.send(attempted_account, verb='attempted to login but failed')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    authentication_classes=[]
    serializer_class=UserRegisterSerializer

"""
class ChangePasswordView(generics.UpdateAPIView):
    
    #An endpoint for changing password.
    
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes=(ExpiringTokenAuthentication,SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""