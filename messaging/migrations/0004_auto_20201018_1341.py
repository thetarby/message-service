# Generated by Django 3.1.2 on 2020-10-18 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_auto_20201018_1336'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blacklist',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='blacklist',
            constraint=models.UniqueConstraint(condition=models.Q(deleted_at=None), fields=('blocking_user', 'blocked_user'), name='unique_blacklist'),
        ),
    ]
