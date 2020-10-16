from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='', null=False, blank=False)
    from_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='by_user')
    to_user =  models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='to_user')
    is_deleted = models.BooleanField(default=False, null=False)
    