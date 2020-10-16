from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance) 
class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #NOTE: do validation on the serializers only maybe?
    phone_regex = RegexValidator(regex=r'^[1-9]\d{1,14}$',
                                 message="Mobile number must be entered in the format:"
                                         " '905000000000'")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, default=None, null=True)
