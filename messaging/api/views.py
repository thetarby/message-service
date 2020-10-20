from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import status,generics, viewsets, serializers
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404 
from django.views.defaults import bad_request
from django.db import IntegrityError

from messaging.services import MessageService
from messaging.api.serializers import *
from messaging.models import *

from django_filters import rest_framework as filters


class MessageViewSet(  mixins.CreateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    View to manage messages.

    POST will create a new message.
    GET will list all messages sent and received by requesting user
    """
    class FilterClass_(filters.FilterSet):
        only_received=filters.BooleanFilter(method='filter_only_received')
        only_sent=filters.BooleanFilter(method='filter_only_sent')
        until=filters.DateTimeFilter(field_name='created_at', lookup_expr='lt')
        since=filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

        def filter_only_received(self, queryset, name, value):
            if value:
                return queryset.filter(to_user=self.request.user)
            else:
                return queryset

        def filter_only_sent(self, queryset, name, value):
            if value:
                return queryset.filter(from_user=self.request.user)
            else:
                return queryset

        class Meta:
            model = Message
            fields = {
                'from_user': ['exact', 'in'],
            }


    permission_classes= (IsAuthenticated,)
    authentication_classes=(TokenAuthentication, SessionAuthentication, )
    queryset=Message.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FilterClass_
    
    class MessageSerializer_(SlugRelatedMessageSerializer):
        class Meta:
            model=Message
            fields=['content', 'to_user']
    serializer_class=MessageSerializer_

    def create(self, request, format=None):
        """
        creates a new message. it does the same thing as sending a message
        """
        print('JKALJDSKHLJLKASDJASKLJDKŞLASKDSKAŞLDKASLD', request.data)
        serializer=SlugRelatedMessageSerializer(data={
            'to_user':request.data['to_user'],
            'from_user':request.user.username,
            'content':request.data['content']
            })
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        m=serializer.save()
        return Response({'message':m.content, 'created_at':m.created_at}, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        list all messages sent or received by requesting user
        """
        messages = MessageService.get_all_messages_of_user(request.user)
        messages = self.filter_queryset(messages)
        return Response(SlugRelatedMessageSerializer(messages, many=True).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        all messages sent by requesting user
        """
        messages = Message.objects.filter(from_user=request.user) | Message.objects.filter(to_user=request.user)
        return Response(SlugRelatedMessageSerializer(messages, many=True).data, status=status.HTTP_201_CREATED)


class Conversation(viewsets.ViewSet):
    """
    View to display conversation with another user
    """
    permission_classes= (IsAuthenticated,)
    authentication_classes=(TokenAuthentication, SessionAuthentication, )
    
    # lookup field when configuring the url with a router
    lookup_field='username'
    
    def get_serializer_class(self):
            if self.action == 'retrieve':
                return MessageSerializer
            elif self.action == 'list':
                return ConversationSerializer
            elif self.action == 'send_message':
                return SlugRelatedMessageSerializer
    
    def retrieve(self, request, username ,format=None):
        """
        returns all messages between user who is requesting and user with the username
        """
        serializer_class = self.get_serializer_class()
        to_user=get_user_model().objects.filter(username=username).first()
        if to_user is None:
            return Response({'error':'No such user'}, status=status.HTTP_404_NOT_FOUND)
        
        messages=MessageService.get_conversation(request.user, to_user)
        return Response(serializer_class(messages, many=True).data, status=status.HTTP_200_OK)

    def list(self, request, format=None):
        """
        returns conversations of the requesting user
        """
        serializer_class = self.get_serializer_class()
        all=MessageService.get_conversations(request.user)
        serializer=serializer_class(all, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    @action(methods=['post'], detail=True, )
    def send_message(self, request, username ,format=None, name='send_message'):
        serializer_class = self.get_serializer_class()
        serializer=serializer_class(data={
            'to_user':username,
            'from_user':request.user.username,
            'content':request.data.get('content', None)
            })
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        m=serializer.save()
        return Response({'message':m.content, 'created_at':m.created_at}, status=status.HTTP_201_CREATED)


class BlacklistViewSet (mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    viewset to manage blacklisting users. 
    
    It is a simple crud logic handled by SlugRelatedBlacklistSerializer hence no need to extend view actions
    """
    
    class Serializer_(SlugRelatedBlacklistSerializer):
        # blocking user will be request.user hence no need to get that information from user.
        # this class extends SlugRelatedBlacklistSerializer and removes blocking user field
        class Meta(SlugRelatedBlacklistSerializer.Meta):
            fields=['blocked_user', 'detail']
    
    serializer_class = Serializer_
    authentication_classes=(TokenAuthentication, SessionAuthentication, )
    permission_classes = [IsAuthenticated]
    lookup_field='blocked_user__username'
    
    def get_queryset(self):
        user = self.request.user
        return Blacklist.objects.filter(blocking_user=user)


class SendMessageWithUserName(APIView):
    """
    Deprecated
    """
    permission_classes= (IsAuthenticated,)
    authentication_classes=(TokenAuthentication, SessionAuthentication, )
    
    # this is only for browsable api to be able to render a form
    serializer_class=type('_', (serializers.Serializer,), {'receiver_username':serializers.CharField(),'content':serializers.CharField()})

    def post(self, request, format=None):
        serializer=SlugRelatedMessageSerializer(data={
            'to_user':request.data['receiver_username'],
            'from_user':request.user.username,
            'content':request.data['content']
            })
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        m=serializer.save()
        return Response({'message':m.content, 'created_at':m.created_at}, status=status.HTTP_201_CREATED)

