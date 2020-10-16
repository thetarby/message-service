from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import UserProfile


class SuperUserUsernamePasswordAuthSerializer(serializers.Serializer):
    """validates username, password and if username, password is correct and user is a superuser, it sets user attribute in validated_data"""
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        

        if user.is_superuser:
            attrs['user'] = user
            return attrs
        else:
            msg = _('Account is not a superuser')
            raise serializers.ValidationError(msg, code='authorization')



class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)