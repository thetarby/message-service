from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models.constraints import UniqueConstraint

# Create your models here.
class Message(models.Model):
    content = models.TextField(default='', null=False, blank=False)
    from_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='sent_messages')
    to_user =  models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='received_messages')
    #is_read = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, null=False)


class Blacklist(models.Model):
    # user who is blocking
    blocking_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='blocked_users')
    # user who is blocked 
    blocked_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='blocked_by_users')
    #reason = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #if null then it is not deleted
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['blocking_user', 'blocked_user'],
                             condition=Q(deleted_at=None),
                             name='unique_blacklist'),
        ]