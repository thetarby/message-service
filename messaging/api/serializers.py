from django.contrib.auth import get_user_model

from rest_framework import serializers

from messaging.models import Message, Blacklist
from messaging.services import MessageService

class UserBlockedError(serializers.ValidationError):
    """
    This class is used to check internally whether the cause of validation error is a blocked user.

    As the error message it does not return the cause of error hence a user cannot understand someone is blocked him or her.
    """
    pass


class MessageSerializer(serializers.ModelSerializer):
    """
    default message serializer with no extra functionality. Useful for direct crud operations.
    """
    sent_date = serializers.DateTimeField(read_only=True, source='created_at')
    class Meta:
        model=Message
        fields=['from_user', 'to_user', 'content', 'sent_date']


    def validate(self, data):
        if MessageService.is_user_blocked(data['from_user'], data['to_user']):
            raise UserBlockedError('message cannot be sent')
        else:
            return data


class SlugRelatedMessageSerializer(MessageSerializer):
    """
    extends default message serializer. Instead of pk field of from_user and to_user, it uses username field's value
    """
    from_user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='username')
    to_user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='username')


class SendMessageSerializer(serializers.Serializer):
    sender_username = serializers.CharField(write_only=True)
    receiver_username = serializers.CharField(write_only=True)
    content = serializers.CharField()

    def validate(self, data):
        """
        validates if sender can send message to reciver. If so sets from_user and to_user attributes inspired by rest_frameworks source code
        """
        User=get_user_model()
        try:
            sender=User.objects.get(username=data.get('sender_username'))
            receiver=User.objects.get(username=data.get('receiver_username'))
        except User.DoesNotExist:
            raise serializers.ValidationError('user does not exist')
            
        if MessageService.is_user_blocked(sender, receiver):
            raise UserBlockedError('message cannot be sent')
        else:
            data['from_user']=sender
            data['to_user']=receiver
            return data


    def save(self, *args, **kwargs):
        success, message=MessageService.send_message(self.validated_data['from_user'], \
                                            self.validated_data['to_user'], \
                                            self.validated_data['content'])
        return success, message


class BlacklistSerializer(serializers.ModelSerializer):
    blocked_username = serializers.CharField(read_only=True, source='blocked_user.username')
    class Meta:
        model=Blacklist
        fields=['blocked_user', 'blocked_username']
    
    def to_internal_value(self, data):
        r=self.context.get('request', None)
        return super().to_internal_value({'blocked_user':data['blocked_user'], 'blocking_user':r.user.pk})

    def save(self):
        Blacklist.objects.create(**{'blocking_user':self.context['request'].user, 'blocked_user':self.validated_data['blocked_user']})


class SlugRelatedBlacklistSerializer(serializers.ModelSerializer):
    blocked_user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='username')
    blocking_user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='username')
    detail = serializers.HyperlinkedRelatedField(
        read_only=True, 
        view_name='blacklist-detail',
        source = 'blocked_user', 
        lookup_field='username',
        lookup_url_kwarg='blocked_user__username')

    class Meta:
        model=Blacklist
        fields=['blocked_user', 'blocking_user' ,'detail']

    def validate(self, attrs):
        if MessageService.is_user_blocked(attrs['blocked_user'], self.context['request'].user):
            raise serializers.ValidationError('User is already blocked')
        return attrs
    
    def save(self):
        # saving serializer blocks user
        return MessageService.block_user(self.context['request'].user, self.validated_data['blocked_user'])


class ConversationSerializer(serializers.Serializer):
    """
    serializes a user instance to a hyperlink for related conversation
    """
    conversation = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='conversation-detail',
        lookup_field='username'
    )

