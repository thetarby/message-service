from messaging.models import *
from django.db.models import Q, Model
from django.db import IntegrityError

class MessageService:
    @staticmethod
    def get_user(user):
        if isinstance(user, str):
            pass
        elif isinstance(user, Model):
            pass
        elif isinstance(user, int):
            pass

    @staticmethod
    def send_message(from_, to_, content):
        """
        method to send a message from a user to another user. Fails if to_user blocked from_user.

        from_:user model that sends message
        to_:user model that receivces message
        content: message content as string

        return value: returns two values (True, message_objects) or (False, Exception) depending on success of operation
        """
        if not MessageService.is_user_blocked(from_, to_):

            MessageService.is_user_blocked(from_, to_)
            message=Message.objects.create(**{
                'from_user':from_,
                'to_user':to_,
                'content':content
            })
            return True, message
        else:
            return False, ''

    
    @staticmethod
    def is_user_blocked(from_user, to_user):
        """
        method to check if a message from from_user to to_user is blacklisted or not 
        """

        # duck typing
        if hasattr(from_user,'pk'):
            if Blacklist.objects.filter(blocked_user=from_user, blocking_user=to_user).exists():
                return True
            else:
                return False
        else:
            if Blacklist.objects.filter(blocked_user__pk=from_user, blocking_user__pk=to_user).exists():
                return True
            else:
                return False

    
    @staticmethod
    def get_conversation(user1, user2, since=None, until=None):
        """
        returns all messages between users user1 and user2. user1 and user2 could be user objects or pk values of them
        """
        date_filter=Q()
        if since is not None:
            date_filter &= Q(created_at__gte=since)
        if until is not None:
            date_filter &= Q(created_at__lte=until)

        return (MessageService.get_sent_messages(user1, user2) | MessageService.get_received_messages(user1, user2)).order_by('created_at') 
        
        # duck typing
        # TODO check for diffrent types
        if hasattr(user1,'pk'):
            messages = Message.objects.filter(from_user__in=[user1, user2], to_user__in=[user1, user2])
        else:
            messages = Message.objects.filter(from_user__pk__in=[user1, user2], to_user__pk__in=[user1, user2])

        return messages.filter(date_filter).order_by('created_at')


    @staticmethod
    def get_sent_messages(sender, receiver, since=None, until=None):
        """
        returns
        """
        date_filter=Q()
        if since is not None:
            date_filter &= Q(created_at__gte=since)
        if until is not None:
            date_filter &= Q(created_at__lte=until)

        # duck typing
        # TODO check for diffrent types
        if hasattr(receiver,'pk'):
            messages = Message.objects.filter(from_user=sender, to_user=receiver)
        else:
            messages = Message.objects.filter(from_user__pk=sender, to_user__pk=receiver)

        return messages.filter(date_filter).order_by('created_at')


    @staticmethod
    def get_received_messages(receiver, sender, since=None, until=None, mark_as_read=False):
        """
        returns
        """
        date_filter=Q()
        if since is not None:
            date_filter &= Q(created_at__gte=since)
        if until is not None:
            date_filter &= Q(created_at__lte=until)

        # duck typing
        # TODO check for diffrent types
        if hasattr(receiver,'pk'):
            messages = Message.objects.filter(from_user=sender, to_user=receiver)
        else:
            messages = Message.objects.filter(from_user__pk=sender, to_user__pk=receiver)

        if mark_as_read:
            messages.update(is_read=True)
        return messages.filter(date_filter).order_by('created_at')
    

    @staticmethod
    def get_conversations(user):
        """
        returns all unique users that user has messaged or been messaged before 
        """
        qs1 = get_user_model().objects.filter(sent_messages__to_user=user)
        qs2 = get_user_model().objects.filter(received_messages__from_user=user)
        return (qs1 | qs2).distinct()

    
    @staticmethod
    def get_all_messages_of_user(user):
        """
        returns all messages of the user(sent and received messages)
        """
        return MessageService.get_all_sent_messages_of_user(user) | MessageService.get_all_received_messages_of_user(user)


    @staticmethod
    def get_all_sent_messages_of_user(user):
        return Message.objects.filter(from_user=user)


    @staticmethod
    def get_all_received_messages_of_user(user):
        return Message.objects.filter(to_user=user)

    @staticmethod
    def block_user(blocking_user, blocked_user):
        """
        method to block a user.

        returns None if blocking user has already blocked blocked_user, otherwise it returns blacklist object
        
        """
        try:
            return Blacklist.objects.create(**{'blocking_user':blocking_user, 'blocked_user':blocked_user})
        except IntegrityError:
            return None