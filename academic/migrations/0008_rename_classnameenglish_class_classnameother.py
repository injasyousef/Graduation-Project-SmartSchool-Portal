# Generated by Django 5.0.4 on 2024-05-19 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0007_assignment_linkinsert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='classNameEnglish',
            new_name='classNameOther',
        ),
    ]
