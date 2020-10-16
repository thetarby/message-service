from messaging.models import *

class MessageService:
    @staticmethod
    def send_message(from_, to_, content):
        """
        method to send a message from a user to another user.

        from_:user model that sends message
        to_:user model that receivces message
        content: message content as string

        return value: returns two values (True, message_objects) or (False, Exception) depending on success of operation
        """
        try:
            message=Message.objects.create(**{
                'from_user':from_,
                'to_user':to_,
                'content':content
            })
            return True, message
        except Exception as e:
            return False, e