from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model,authenticate
from django.db import transaction

from rest_framework import serializers



class UsernamePasswordAuthSerializer(serializers.Serializer):
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
        

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
    )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email_address = serializers.EmailField(required=False)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )    
    password_again = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username=attrs.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError('Another user with the same username exists')
        
        if attrs['password'] != attrs['password_again']:
            raise serializers.ValidationError('Passwords do not match')

        return attrs

    def save(self):
        data=self.validated_data
        with transaction.atomic():
            user=get_user_model().objects.create_user(data['username'], data.get('email_address', None), data['password'])
            user.first_name=data.get('first_name', user.first_name)
            user.last_name=data.get('last_name', user.last_name)
            user=user.save()
        return user 
