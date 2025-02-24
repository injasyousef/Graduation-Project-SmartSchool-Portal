# Generated by Django 5.0.4 on 2024-04-27 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('advertisementID', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employee')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.studyyear')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='title_new_message', max_length=255)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('receiverEmployee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='users.useremployee')),
                ('receiverStudent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='users.userstudent')),
                ('senderEmployee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='users.useremployee')),
                ('senderStudent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='users.userstudent')),
            ],
        ),
    ]
