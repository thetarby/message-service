# Generated by Django 3.1.2 on 2020-10-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0006_auto_20201018_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_deleted',
        ),
        migrations.AddField(
            model_name='message',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
