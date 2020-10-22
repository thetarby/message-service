from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model).filter(deleted_at=None)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeleteModel(models.Model):
    """
    An abstract base model to utilize soft deletion. Instead of actually deleting an object from database, 
    this model sets deleted_at field to the time deletion occurs. And its default manager's base query returns
    a queryset filtering rows whose deleted_at is not null. 
    
    If soft deleted objects is needed <all_objects> manager can be used instead of <objects> manager. 

    If object should actually be deleted then instead of .delete() method, .hard_delete() method can be used.
    """
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


# Create your models here.
class Message(SoftDeleteModel):
    content = models.TextField(default='', null=False, blank=False)
    from_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='sent_messages')
    to_user =  models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='received_messages')
    #is_read = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Blacklist(SoftDeleteModel):
    # user who is blocking
    blocking_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='blocked_users')
    # user who is blocked 
    blocked_user = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='blocked_by_users')
    #reason = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['blocking_user', 'blocked_user'],
                             condition=Q(deleted_at=None), # deleted_at field comes from soft-delete model
                             name='unique_blacklist'),
        ]