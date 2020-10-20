from django.urls import path
from messaging.api.views import *
from rest_framework import generics, routers
from messaging.models import *


router = routers.DefaultRouter(trailing_slash=False)
router.register('blacklist', BlacklistViewSet, basename='blacklist')
router.register('conversation', Conversation, basename='conversation')
router.register('message', MessageViewSet, basename='message')
urlpatterns=[
    
    path('message2',SendMessageWithUserName.as_view(), name='message2'),
    #path('conversation/<username>',Conversation.as_view(), name='conversation'),

]+router.urls

