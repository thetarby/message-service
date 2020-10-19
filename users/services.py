from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model,authenticate
from django.db import transaction

from rest_framework.authtoken.models import Token

from actstream import action

from datetime import datetime, timedelta
import pytz

class UserService:
    
    @staticmethod
    def generate_token_for_user(user, send_actions=True):
        """
        generates auth token for given user. if send_actions is true it records activities.
        """
        token, created =  Token.objects.get_or_create(user=user)
            
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        # TODO: make timedelta optional maybe?
        if not created and token.created < utc_now - timedelta(hours=24):
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.utcnow()
            token.save()
        
        if send_actions:
            action.send(user, verb='logged in')
        return token