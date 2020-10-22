from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Populates db with 10 users'

    def handle(self, *args, **kwargs):
        if get_user_model().objects.count()>0:
            self.stdout.write("There are already users in db. Skipping populating")
            return
        for i in range(10):
            get_user_model().objects.create_user(f'user{i}',f'example{i}@example.com',f'pass12345')