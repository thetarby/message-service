from django.db.models.signals import post_save, post_delete
from actstream import action
from messaging.models import *

def send_message_handler(sender, instance, created, **kwargs):
    action.send(instance.from_user, verb='sent', action_object=instance, target=instance.to_user)

post_save.connect(send_message_handler, sender=Message)


def save_blacklist_handler(sender, instance, created, **kwargs):
    action.send(instance.blocking_user, verb='blocked', target=instance.blocked_user)

post_save.connect(save_blacklist_handler, sender=Blacklist)


def delete_blacklist_handler(sender, instance, **kwargs):
    action.send(instance.blocking_user, verb='unblocked', target=instance.blocked_user)

post_delete.connect(delete_blacklist_handler, sender=Blacklist)