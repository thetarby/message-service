from django.shortcuts import render
from rest_framework import status,generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from users.serializers import *
#from users.authentications import ExpiringTokenAuthentication

from datetime import datetime, timedelta
import pytz

class SuperUserObtainExpiringAuthToken(generics.CreateAPIView):
    """
    Given username and password it returns an access token for the api if it is superuser. No callback token authentication is required.
    This view could be used for admin logins.
    """
    authentication_classes=[]
    serializer_class=SuperUserUsernamePasswordAuthSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
            
            utc_now = datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)
            if not created and token.created < utc_now - timedelta(hours=24):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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