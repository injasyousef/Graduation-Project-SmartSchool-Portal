# Generated by Django 5.0.4 on 2024-07-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0003_advertisement_title_alter_message_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='senderParent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
